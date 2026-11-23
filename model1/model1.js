/* =========================================================
   Last Catch — MODEL 1
   Reads the seller's input into global variables, then scores
   the description from 0 to 10:
     0  = something very bad was said (catch should go grey)
     5  = neutral / nothing important mentioned
     10 = only good things were said (improves the score)
   No API key and no internet needed.
   ========================================================= */

// ---------- Global variables (the seller's input) ----------
let fishType = "";            // string,  e.g. "Snoek"
let weightKg = 0.0;           // double,  e.g. 20.5
let storedInIce = false;      // boolean, true or false
let description = "";         // string,  max 100 characters
let descriptionScore = 5;     // number,  0 - 10 (calculated)
let reasonsFound = [];        // list of what affected the score
let mustGoGrey = false;       // boolean, true if something dangerous was said

const MAX_DESCRIPTION_LENGTH = 100;
const NEUTRAL_SCORE = 5;

// ---------- Word lists: phrase -> points ----------
// Positive points raise the score, negative points lower it.
const GOOD_SIGNS = {
  "gutted": 1, "cleaned": 1, "bled": 1.5,
  "slurry": 2, "ice water": 2, "crushed ice": 1.5, "lots of ice": 1.5,
  "cooler": 0.5, "cool box": 0.5, "shade": 0.5,
  "just caught": 1.5, "this morning": 1, "fresh": 1,
  "firm": 1, "shiny": 1, "clear eyes": 1.5, "red gills": 1.5,
  "offshore": 1, "deep water": 1,
  "cold": 0.5, "overcast": 0.5,
};

const BAD_SIGNS = {
  "bruise": -1, "scratch": -0.5, "soft": -1.5,
  "damage": -1.5, "crushed": -2, "torn": -2,
  "hot": -1, "sunny": -0.5, "warm": -0.5, "heatwave": -2.5,
  "harbour": -1, "harbor": -1, "estuary": -0.5,
  "yesterday": -2, "overnight": -1.5,
  "cloudy eyes": -2, "brown gills": -2, "slimy": -2,
};

// Anything here forces a score of 0, so the catch goes grey (not safe to eat)
const DANGER_SIGNS = [
  "sewage", "outfall", "red tide", "algal bloom", "toxic",
  "dead fish", "rotten", "smells bad", "bad smell", "ammonia",
  "fuel spill", "oil spill", "chemical",
];

const NEGATION_WORDS = ["no", "not", "without", "never"];


// ---------- Step 1: store the input in the global variables ----------
function setInput(type, weight, iced, desc) {
  fishType = String(type).trim();
  weightKg = parseFloat(weight);                  // turns "20.5" into 20.5
  storedInIce = (iced === true || iced === "true" || iced === "yes");
  description = String(desc || "").trim().slice(0, MAX_DESCRIPTION_LENGTH);

  if (fishType === "") return "Please enter a fish type.";
  if (isNaN(weightKg) || weightKg <= 0) return "Weight must be a number above 0.";
  return "ok";
}


// ---------- Step 2: helpers ----------
// Finds a whole word or phrase, allowing endings like s / d / es / ed ("bruise" matches "bruised")
function findPhrase(text, phrase) {
  const pattern = new RegExp("\\b" + phrase + "(s|d|es|ed)?\\b");
  const match = text.match(pattern);
  return match ? match.index : -1;          // position in the text, or -1 if not found
}

// Checks if a negation word comes right before the phrase ("no damage", "not soft")
function isNegated(text, phrase) {
  const index = findPhrase(text, phrase);
  const before = text.slice(Math.max(0, index - 12), index);
  return NEGATION_WORDS.some(word => new RegExp("\\b" + word + "\\s").test(before));
}

function mentions(text, phrase) { return findPhrase(text, phrase) !== -1; }


// ---------- Step 3: score the description from 0 to 10 ----------
function scoreDescription() {
  const text = description.toLowerCase();
  let score = NEUTRAL_SCORE;
  reasonsFound = [];
  mustGoGrey = false;

  // 3a. Dangerous signs: score 0, stop immediately
  for (const phrase of DANGER_SIGNS) {
    if (mentions(text, phrase) && !isNegated(text, phrase)) {
      mustGoGrey = true;
      reasonsFound.push("DANGER: " + phrase);
    }
  }
  if (mustGoGrey) {
    descriptionScore = 0;
    return descriptionScore;
  }

  // 3b. Good signs raise the score (a negated good sign lowers it a little)
  for (const phrase in GOOD_SIGNS) {
    if (mentions(text, phrase)) {
      if (isNegated(text, phrase)) {
        score -= GOOD_SIGNS[phrase] / 2;
        reasonsFound.push("not " + phrase + " (" + (-GOOD_SIGNS[phrase] / 2) + ")");
      } else {
        score += GOOD_SIGNS[phrase];
        reasonsFound.push(phrase + " (+" + GOOD_SIGNS[phrase] + ")");
      }
    }
  }

  // 3c. Bad signs lower the score (a negated bad sign, like "no bruises", is ignored)
  for (const phrase in BAD_SIGNS) {
    if (mentions(text, phrase) && !isNegated(text, phrase)) {
      score += BAD_SIGNS[phrase];
      reasonsFound.push(phrase + " (" + BAD_SIGNS[phrase] + ")");
    }
  }

  // 3d. Keep the score between 0 and 10
  descriptionScore = Math.round(Math.min(10, Math.max(0, score)) * 10) / 10;
  return descriptionScore;
}


// ---------- Run everything at once ----------
function runModel1(type, weight, iced, desc) {
  const check = setInput(type, weight, iced, desc);
  if (check !== "ok") return { ok: false, error: check };
  scoreDescription();
  return {
    ok: true,
    fishType, weightKg, storedInIce, description,
    descriptionScore, mustGoGrey, reasonsFound,
  };
}

// Lets you test it in Node: node model1.js
if (typeof module !== "undefined") module.exports = { runModel1 };
