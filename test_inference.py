from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import unicodedata

def normalize_text(s):
    return unicodedata.normalize("NFKD", s).replace("’", "'").lower()


NEGATIONS = [
    "not", "n't", "no", "never", "hardly", "barely", 
    "without", "none", "nothing", "nowhere"
]

best_thresholds = {
    "admiration": 0.45, "amusement": 0.25, "anger": 0.50, "annoyance": 0.25,
    "approval": 0.30, "caring": 0.25, "confusion": 0.30, "curiosity": 0.30,
    "desire": 0.10, "disappointment": 0.15, "disapproval": 0.20, "disgust": 0.20,
    "embarrassment": 0.25, "excitement": 0.25, "fear": 0.40, "gratitude": 0.50,
    "grief": 0.30, "joy": 0.35, "love": 0.50, "nervousness": 0.20,
    "optimism": 0.30, "pride": 0.05, "realization": 0.25, "relief": 0.05,
    "remorse": 0.35, "sadness": 0.40, "surprise": 0.15, "neutral": 0.25
}

labels = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", 
    "confusion", "curiosity", "desire", "disappointment", "disapproval", "disgust",
    "embarrassment", "excitement", "fear", "gratitude", "grief", "joy",
    "love", "nervousness", "optimism", "pride", "realization", "relief",
    "remorse", "sadness", "surprise", "neutral"
]

meta_emotions = {
    "passive_frustration": ["approval", "disappointment", "annoyance", "disapproval"],
    "positive_excited": ["admiration", "excitement", "joy", "pride"],
    "negative_strong": ["anger", "disgust", "fear"],
    "sad_block": ["sadness", "grief", "remorse"],
    "care_block": ["caring", "love", "gratitude"],
    "confusion_block": ["confusion", "realization", "curiosity"],
    "burnout_exhaustion": ["sadness", "disappointment", "annoyance"],
    "anxiety_block": ["fear", "nervousness"],
    "calm_relief": ["relief", "joy"],  # SADECE relief + joy (approval/neutral kaldır)
    "detachment": ["neutral", "disappointment"],
    "desire_block": ["desire", "curiosity"],
    "humor_light": ["amusement"],
    "positive_mild": ["optimism", "approval"]  # yeni grup
}

ANXIETY_PHRASES_V2 = [
    "can't stop overthinking", "can't stop thinking", 
    "mind won't shut up", "thoughts racing", "on edge", 
    "can't calm", "worried I'll", "what if",
    "thoughts won't stop", "feel on edge", "won't shut up",
    "racing", "constantly on edge", "thoughts won't stop racing",
    "my thoughts", "thoughts won't"  # eklendi - daha geniş eşleşme
]

def anxiety_phrase_rule(text):
    t = normalize_text(text)
    
    # Romantic/positive → desire
    if "can't stop thinking" in t and "you" in t:
        return "desire_block"
    
    # Anxiety patterns - GENİŞLETİLDİ
    anxiety_keywords = ["racing", "on edge", "overthinking", "won't shut up", "can't calm"]
    if any(kw in t for kw in anxiety_keywords):
        return "anxiety_block"
    
    # Orijinal pattern check
    if any(p in t for p in ANXIETY_PHRASES_V2):
        negative_objects = ["it", "this", "everything", "the situation", "my life", "all of that", "my mind", "my thoughts"]
        if any(obj in t for obj in negative_objects):
            return "anxiety_block"
    
    if "can't help" in t:
        if "wanting" in t or "desire" in t or "wish" in t:
            return "desire_block"  # CHANGED from "desire"
    
    return None

def has_negation(text_l, word):
    tokens = text_l.split()
    for i, tok in enumerate(tokens):
        if tok == word:
            window = tokens[max(0, i-4):i]
            if any(n in window for n in NEGATIONS):
                return True
    return False

POSITIVE_WORDS = [
    "smile", "smiling", "happy", "excited", "made my day",
    "so good", "energized", "buzzing", "omg", "literally"  # added omg, literally
]

def positive_override(text_l, probs, labels):
    for p in POSITIVE_WORDS:
        if p in text_l:
            if not has_negation(text_l, p):
                return "positive_excited"
    return None

CALM_WORDS = ["calm", "peaceful", "relieved", "relief", "breathe", "breathing", "finally breathe", "feel calm"]

def calm_rule(text_l, active):
    # Önce sarcasm check
    sarcasm_markers = ["whatever", "i guess", "anyway", "go ahead", "i'm done", "just done"]
    if any(s in text_l for s in sarcasm_markers):
        return None  # calm değil
    
    for c in CALM_WORDS:
        if c in text_l and not has_negation(text_l, c):
            # Text-only calm detection (model boşsa)
            if len(active) == 0 or (len(active) == 1 and "neutral" in active):
                return "calm_relief"
            
            # Model-based calm
            if active.get("relief", 0) > 0.10 or active.get("joy", 0) > 0.35:
                return "calm_relief"
    return None

CARE_WORDS = ["love", "care", "grateful", "appreciate", "mean a lot", "means a lot", "didn't have to"]

def care_rule(text_l, active):
    # ÖNCE SARCASM/NEGATION CHECK - GENİŞLETİLDİ
    # "no worries" with "don't have to" = sarcasm, skip care detection
    if "no worries" in text_l and ("don't have to" in text_l or "you don't have to" in text_l):
        return None  # let passive_frustration handle it
    
    # "don't have to care" - specific negation
    if "don't have to care" in text_l or "you don't have to care" in text_l:
        return None  # skip care detection
    
    # General "don't have to" check - MOVED AFTER specific checks
    if "don't have to" in text_l or "you don't have to" in text_l:
        # If it's followed by a care word, skip
        if any(cw in text_l for cw in CARE_WORDS):
            return None
    
    for cw in CARE_WORDS:
        if cw in text_l:
            if has_negation(text_l, cw):
                return None
            
            # care_block koşulu
            if active.get("gratitude", 0) > 0.15 or active.get("caring", 0) > 0.15:
                return "care_block"
            
            # Text-only care
            if len(active) <= 1:
                return "care_block"
    return None


def passive_frustration_text_rule(text, probs, labels):
    t = normalize_text(text)

    patterns = [
        "i'm not mad",
        "i am not mad",
        "i'm not upset",
        "i'm just tired",
        "i am just tired",
        "done explaining myself",
        "whatever you want",
        "i don't care anymore",
        "it's fine i guess",
    ]

    if not any(p in t for p in patterns):
        return None

    anger = probs[labels.index("anger")].item()
    sadness = probs[labels.index("sadness")].item()
    joy = probs[labels.index("joy")].item()
    neutral = probs[labels.index("neutral")].item()

    if neutral > 0.60:
        weak = ["annoyance", "disappointment", "disapproval"]
        if any(probs[labels.index(w)].item() > 0.10 for w in weak):
            return "passive_frustration"
    return None



def passive_frustration_rule(text_l, probs, labels, active):
    sarcasm_markers = ["whatever", "i guess", "sure", "obviously", "go ahead", "fine"]
    
    # Sarcasm varsa joy/excitement'a dikkat et
    if any(s in text_l for s in sarcasm_markers):
        # "makes you happy" kontrolü KALDIRILDI - çünkü sarcasm yine de PF
        # Eğer güçlü positive var ama weak negative de var → PF
        if active.get("joy", 0) > 0.40 or active.get("excitement", 0) > 0.40:
            weak = ["annoyance", "disappointment", "disapproval"]
            if any(active.get(w, 0) > 0.10 for w in weak):
                return "passive_frustration"
        
        # Sadece weak negatives → PF
        weak = ["annoyance", "disappointment", "disapproval"]
        if any(active.get(w, 0) > 0.10 for w in weak):
            return "passive_frustration"
        
        # SARCASM VAR AMA ZAYIF EMOTION → YİNE PF (YENİ)
        if active.get("joy", 0) > 0.30 or active.get("approval", 0) > 0.30:
            return "passive_frustration"
    
    return None

def special_passive_frustration_rule(active, probs, labels):
    """Weak PF signals via approval + neutral combo"""
    if active.get("approval", 0) > 0.50 and active.get("neutral", 0) > 0.20:
        weak = ["annoyance", "disappointment", "disapproval"]
        if any(active.get(w, 0) > 0.10 for w in weak):
            return "passive_frustration"
    return None


def surprise_rule(active):
    if "surprise" in active:
        # surprise + joy/excitement → positive_excited
        if active.get("joy", 0) > 0.25 or active.get("excitement", 0) > 0.25:
            return "positive_excited"

        # surprise + neutral → hafif pozitif
        if "neutral" in active:
            return "calm_relief"

        # sadece surprise → hafif pozitif
        return "calm_relief"

BURNOUT_PHRASES = [
    "feel numb", "feel empty", "feel drained", "feel exhausted",
    "feel overwhelmed", "running on empty", "can't anymore",
    "feel pointless", "it's pointless", "feels pointless",
    "i'm numb", "nothing affects", "don't feel anything", "just existing",
    "no energy", "don't have the energy",
    "feel anything"  # added - catches "don't really feel anything"
]

def burnout_rule(text_l, active):
    if any(p in text_l for p in BURNOUT_PHRASES):
        # Eğer sadness/disappointment az da olsa varsa
        if active.get("sadness", 0) > 0.05 or active.get("disappointment", 0) > 0.05:
            return "burnout_exhaustion"
        # Hiç emotion yoksa bile burnout olabilir
        if len(active) == 0 or active.get("neutral", 0) > 0.30:  # lowered from 0.50
            return "burnout_exhaustion"
    return None

DESIRE_WORDS = ["drawn to", "want this", "can't help wanting"]  # new

def desire_rule(text_l, active):
    """Detect desire from text patterns"""
    for dw in DESIRE_WORDS:
        if dw in text_l:
            return "desire_block"
    return None

def map_to_meta_emotion(text, probs, labels, meta_map, class_thresholds):
    text_l = normalize_text(text)
    
    # 1. ACTIVE emotions
    active = {
        labels[i]: probs[i].item()
        for i in range(len(labels))
        if probs[i].item() > class_thresholds[labels[i]]
    }
    
    # 2. MODEL CONFIDENCE
    max_prob = probs.max().item()
    is_confident = max_prob > 0.70  # 0.75 → 0.70 düşürüldü
    
    # ============================================
    # LAYER 1: CRITICAL TEXT PATTERNS
    # ============================================
    # Burnout
    burnout = burnout_rule(text_l, active)
    if burnout:
        if "just existing" in text_l:  # always burnout
            return burnout, active, {}
        if not is_confident or active.get("sadness", 0) > 0.20:
            return burnout, active, {}
    
    # Anxiety
    anxiety = anxiety_phrase_rule(text)
    if anxiety and (not is_confident or active.get("fear", 0) > 0.40):
        return anxiety, active, {}
    
    # ============================================
    # LAYER 2: MODEL-DOMINANT
    # ============================================
    if is_confident:
        meta_scores = {meta: 0 for meta in meta_map}
        for meta, group in meta_map.items():
            for lbl in group:
                if lbl in active:
                    meta_scores[meta] += active[lbl]
        
        best_meta = max(meta_scores, key=meta_scores.get)
        
        # CARE OVERRIDE (YENİ)
        care_signals = active.get("gratitude", 0) + active.get("caring", 0) + active.get("love", 0)
        if care_signals > 0.50:
            return "care_block", active, meta_scores
        
        # Admiration + care text
        if active.get("admiration", 0) > 0.70 and any(cw in text_l for cw in CARE_WORDS):
            return "care_block", active, meta_scores
        
        # Fear priority
        if active.get("fear", 0) > 0.70:
            if active.get("nervousness", 0) > 0.30:
                return "anxiety_block", active, meta_scores
            return "negative_strong", active, meta_scores
        
        # Surprise
        if "surprise" in active and active["surprise"] > 0.70:
            if active.get("joy", 0) > 0.25 or active.get("excitement", 0) > 0.25:
                return "positive_excited", active, meta_scores
            return "calm_relief", active, meta_scores
        
        return best_meta, active, meta_scores
    
    # ============================================
    # LAYER 3: RULE-ASSISTED
    # ============================================
    pf = passive_frustration_text_rule(text, probs, labels)
    if pf:
        return pf, active, {}
    
    pf_special = passive_frustration_rule(text_l, probs, labels, active)
    if pf_special:
        return pf_special, active, {}
    
    pos = positive_override(text_l, probs, labels)
    if pos:
        return pos, active, {}
    
    des = desire_rule(text_l, active)
    if des:
        return des, active, {}
    
    care = care_rule(text_l, active)
    if care:
        return care, active, {}
    
    calm = calm_rule(text_l, active)
    if calm:
        return calm, active, {}
    
    # ============================================
    # LAYER 4: FALLBACK
    # ============================================
    if list(active.keys()) == ["neutral"]:
        return "neutral", active, {}
    
    if len(active) == 1:
        single = next(iter(active.keys()))
        for meta, group in meta_map.items():
            if single in group:
                return meta, active, {}
    
    if len(active) == 0:
        return "neutral", {}, {}
    
    meta_scores = {meta: 0 for meta in meta_map}
    for meta, group in meta_map.items():
        for lbl in group:
            if lbl in active:
                meta_scores[meta] += active[lbl]
    
    best_meta = max(meta_scores, key=meta_scores.get)
    return best_meta, active, meta_scores

# ------------------------
#  TOPLU TEST LİSTESİ
# ------------------------
# Normal + Edge Case Mix (50/50)
tests = [
    # ===== NORMAL CASES (model güçlü) =====
    # Clear positive
    "I'm so happy right now!",
    "This is amazing, I love it!",
    "You made my day, thank you!",
    "I'm feeling great today.",
    "Wow, this is incredible!",
    "I'm really excited about this.",
    "That's so cool!",
    "I'm proud of you!",
    "This makes me smile.",
    "I appreciate this so much.",
    
    # Clear negative
    "I'm really angry about this.",
    "This makes me so mad.",
    "I hate this situation.",
    "I'm disgusted by this behavior.",
    "This is terrible.",
    "I'm scared right now.",
    "I feel sick about this.",
    "This is infuriating.",
    "I'm furious.",
    "That's completely unacceptable.",
    
    # Clear sadness
    "I'm really sad today.",
    "I miss them so much.",
    "This breaks my heart.",
    "I feel so alone.",
    "I'm grieving.",
    "I feel heartbroken.",
    "I'm crying right now.",
    "This hurts so much.",
    
    # Clear gratitude/care
    "Thank you so much!",
    "I'm grateful for you.",
    "I really appreciate this.",
    "You're so kind.",
    "I love you.",
    "I care about you deeply.",
    "You mean the world to me.",
    
    # Clear confusion
    "I'm confused.",
    "I don't understand this.",
    "What does this mean?",
    "I'm puzzled.",
    "This doesn't make sense.",
    
    # Clear surprise
    "Oh wow!",
    "I didn't expect this!",
    "What a surprise!",
    "I'm shocked!",
    
    # ===== EDGE CASES (rule-heavy) =====
    # Passive frustration (sarcasm)
    "I mean, do whatever you want, I don't expect anything anymore.",
    "It's fine, I'm used to being disappointed honestly.",
    "I'm not mad, I'm just tired of explaining myself.",
    "Sure, it's okay, I guess I'm wrong again.",
    "No worries, you don't have to care.",
    "Yeah sure, whatever makes you happy I guess.",
    "No really, I'm totally fine. Obviously.",
    "It's whatever, I'm done caring.",
    "Whatever, I'm used to this shit.",
    "Sure, because I'm always the one who's wrong.",
    "It's fine. I'm fine. Everything is fine.",
    "Yeah, go ahead, do your thing.",
    "I guess it doesn't matter anymore.",
    "I think I'm just done.",
    
    # Burnout (nuanced sadness)
    "I don't know, I just feel empty.",
    "I'm trying to stay strong but it's pointless.",
    "I'm so tired of feeling tired.",
    "I feel drained every single day.",
    "I don't have the energy to fight",
    "I feel numb lately.",
    "I miss feeling motivated.",
    "I feel like I'm running on empty.",
    "It's whatever, I don't really feel anything.",
    "I don't feel connected to people anymore.",
    "I just feel distant.",
    "I'm numb, honestly.",
    "Nothing affects me anymore.",
    "I'm just existing.",
    "I feel broken honestly.",
    "I don't feel like myself lately.",
    "I miss who I used to be.",
    
    # Anxiety (specific patterns)
    "I can't stop thinking about it.",
    "I can't stop overthinking everything.",
    "My mind won't shut up.",
    "My thoughts won't stop racing.",
    "I feel on edge constantly.",
    "I'm worried I'll mess everything up.",
    "I can't calm my mind.",
    "I can't stop thinking about the situation.",
    
    # Desire (ambiguous want)
    "I want this a lot more than I should.",
    "I can't help wanting this.",
    "I'm really drawn to this.",
    "I wish things didn't hurt so much.",
    
    # Care ambiguity
    "You didn't have to but it means a lot.",
    "You mean a lot to me.",
    
    # Positive excited (high energy)
    "OMG you actually did it! This is insane!",
    "I seriously can't stop smiling right now.",
    "I'm feeling super energized today.",
    "Great job!! I'm so excited for you!",
    "Omg this news just made my day!",
    "I can't believe this is happening, I'm so hyped.",
    "You absolutely killed it, I'm so proud.",
    "This is insane, let's celebrate!",
    "I'm so excited I can't sit still.",
    "This is the best thing ever!",
    "I'm literally buzzing with energy.",
    "I can't stop smiling omg.",
    "This feels really good.",
    
    # Calm/relief
    "Wow, what a nice surprise!",
    "I feel peaceful finally.",
    "I'm relieved it's over.",
    "Everything feels calm again.",
    "I can finally breathe.",
    "I think things will be okay.",
    
    # Detachment
    "I didn't expect anything from you anyway.",
    "I didn't mean anything to you anyway.",
    "Do whatever you want, like always.",
    "I think I'm missing something.",
    "I swear you're pushing my limits.",
    
    # Other edge cases
    "If you talk to me like that again I'll snap.",
    "This is absolutely disgusting.",
    "I'm terrified of what could happen.",
    "Stop lying to me, it pisses me off.",
    "That was extremely disrespectful.",
    "I miss how things used to be.",
    "I regret everything.",
    "This makes no sense to me.",
    "This feels unreal I swear.",
    "I appreciate you more than you know.",
    "I feel really cared for.",
    "I'm confused… did I misunderstand something?",
    "Wait—what just happened?",
    "I don't get it, something feels off.",
    "I just realized something important.",
    "I'm curious now actually.",
    "I'm curious and I want more.",
    "I'm scared something bad will happen.",
    "This makes me sick.",
    "I feel angry just thinking about it.",
    "I'm shaking from fear.",
    "You seriously disgust me sometimes.",
    "I'm terrified right now.",
    "I'm scared of losing everything.",
    "This whole situation is exhausting.",
    "Forget it. I won't say anything.",
]


# ------------------------
#  MODELİ YÜKLE
# ------------------------
tokenizer = DistilBertTokenizer.from_pretrained("./model")
model = DistilBertForSequenceClassification.from_pretrained("./model")

# ------------------------
#  TOPLU ÇALIŞTIRMA
# ------------------------
print("\n======= BULK TEST RESULT =======\n")

# METRIK TRACKING
model_dominant_count = 0
rule_assisted_count = 0
confidence_scores = []

for i, text in enumerate(tests, 1):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.sigmoid(outputs.logits)[0]

    max_prob = probs.max().item()
    confidence_scores.append(max_prob)
    
    # Decision tracking
    is_confident = max_prob > 0.70
    
    if is_confident:
        model_dominant_count += 1
        decision_type = "🤖 MODEL-DOMINANT"
    else:
        rule_assisted_count += 1
        decision_type = "📋 RULE-ASSISTED"
    
    meta, active, meta_scores = map_to_meta_emotion(
        text, probs, labels, meta_emotions, best_thresholds
    )

    print(f"\n[{i}] {decision_type} (confidence: {max_prob:.3f})")
    print(f"TEXT → {text}")
    print("Active:", active)
    print("META:", meta)
    print("----------------------------------------")

# ------------------------
#  SUMMARY STATISTICS
# ------------------------
print("\n" + "="*60)
print("📊 DECISION DISTRIBUTION")
print("="*60)
print(f"🤖 Model-Dominant (max_prob > 0.75): {model_dominant_count}/{len(tests)} ({model_dominant_count/len(tests)*100:.1f}%)")
print(f"📋 Rule-Assisted (max_prob < 0.75):  {rule_assisted_count}/{len(tests)} ({rule_assisted_count/len(tests)*100:.1f}%)")
print(f"\n📈 Confidence Stats:")
print(f"   Average: {sum(confidence_scores)/len(confidence_scores):.3f}")
print(f"   Min: {min(confidence_scores):.3f}")
print(f"   Max: {max(confidence_scores):.3f}")
print(f"   Median: {sorted(confidence_scores)[len(confidence_scores)//2]:.3f}")

# Histogram gösterimi (opsiyonel)
print(f"\n📊 Confidence Distribution:")
bins = [0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1.0]
for i in range(len(bins)-1):
    count = sum(1 for c in confidence_scores if bins[i] <= c < bins[i+1])
    bar = "█" * count
    print(f"   {bins[i]:.2f}-{bins[i+1]:.2f}: {bar} ({count})")

print("="*60)

# Test different thresholds
for threshold in [0.70, 0.75, 0.80]:
    model_count = sum(1 for c in confidence_scores if c > threshold)
    rule_count = len(confidence_scores) - model_count
    print(f"\nThreshold {threshold}: Model={model_count} ({model_count/len(tests)*100:.1f}%), Rules={rule_count} ({rule_count/len(tests)*100:.1f}%)")
