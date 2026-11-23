/* =========================================================
   Last Catch — MODEL 2 (runs the trained model in the browser)
   Needs: model1/model1.js (global variables) and model2/model2_data.js (trained weights)

   b = starting score, from Model 1's descriptionScore and mustGoGrey
   m = spoilage rate per hour, from the trained regression
   score(x) = b * e^(-m * x)        x = hours since caught ln regression for curve as time increases bacteria increases much more so it is much more unsafe to consume 
   ========================================================= */

// ---------- Global variables filled by Model 2 ----------
let fishGroup = "";        // e.g. "oily_pelagic"
let fatLevel = 1;          // 0 lean, 1 medium, 2 high
let hoursSinceCaught = 0;  // double
let b = 0;                 // starting score (0 - 100)
let m = 0;                 // spoilage rate per hour
let currentScore = 0;      // score right now (0 - 100)
let hoursLeft = 0;         // hours until the catch goes grey

const KEYWORD_GROUPS = [
  ["tuna","scombroid"],["mackerel","scombroid"],["shark","cartilaginous"],["ray","cartilaginous"],
  ["lobster","crustacean"],["crab","crustacean"],["prawn","crustacean"],["shrimp","crustacean"],
  ["mussel","bivalve"],["oyster","bivalve"],["clam","bivalve"],["squid","cephalopod"],
  ["trout","freshwater"],["bass","lean_white"],["bream","lean_white"],
];

function lookupFish(name) {
  const key = name.trim().toLowerCase();
  if (!key) return { group: "oily_pelagic", fat: 1 };
  // 1. exact match, 2. partial match ("Blue Marlin" -> Marlin, "Mussels" -> Mussel), longest name first
  const byLength = [...MODEL2_DATA.fish].sort((a, b) => b.name.length - a.name.length);
  const found = MODEL2_DATA.fish.find(f => f.name.toLowerCase() === key)
             || byLength.find(f => key.includes(f.name.toLowerCase()));
  if (found) return { group: found.group, fat: found.fat };
  for (const [word, group] of KEYWORD_GROUPS) if (key.includes(word)) return { group, fat: 1 };
  return { group: "oily_pelagic", fat: 1 };          // unknown fish: assume faster spoilage
}

function initialScore(descScore, grey) {           // same formula as train_model2.py
  return grey ? 0 : 75 + 2.5 * descScore;
}

function predictM(group, fat, iced, descScore, weight) {
  const features = MODEL2_DATA.groups.map(g => (g === group ? 1 : 0))
    .concat([fat, iced ? 1 : 0, descScore, Math.log(Math.max(weight, 0.1))]);
  let logM = MODEL2_DATA.intercept;
  features.forEach((value, i) => { logM += value * MODEL2_DATA.coefficients[i]; });
  return Math.exp(logM);
}

const scoreAt = (hours) => b * Math.exp(-m * hours);

function stageFor(score) {
  if (score >= 85) return { name: "Freshest",        color: "#2ecc71" };
  if (score >= 70) return { name: "Good",            color: "#f1c40f" };
  if (score >= 55) return { name: "Sell soon",       color: "#e67e22" };
  if (score >= MODEL2_DATA.safe_cutoff) return { name: "Last call", color: "#e74c3c" };
  return { name: "By-product only", color: "#7f8c8d" };
}

// Run after runModel1(), so the Model 1 global variables are filled in
function runModel2(hours) {
  hoursSinceCaught = Math.max(0, parseFloat(hours) || 0);
  caughtAt = caughtAtFromHoursAgo(hoursSinceCaught);        // save the exact time caught
  const fish = lookupFish(fishType);                         // fishType from Model 1
  fishGroup = fish.group; fatLevel = fish.fat;
  b = initialScore(descriptionScore, mustGoGrey);            // from Model 1
  m = predictM(fishGroup, fatLevel, storedInIce, descriptionScore, weightKg);
  currentScore = scoreAt(hoursSinceCaught);
  const cutoff = MODEL2_DATA.safe_cutoff;
  hoursLeft = b <= cutoff ? 0 : Math.max(0, Math.log(b / cutoff) / m - hoursSinceCaught);
  return { fishGroup, b, m, currentScore, hoursLeft, stage: stageFor(currentScore) };
}

// ---------- TIME TRACKING ----------
// x is no longer typed in once: it's measured from the moment the fish was caught.
let caughtAt = 0;              // timestamp (milliseconds) when the fish was caught
const MS_PER_HOUR = 3600 * 1000;

// "caught 2 hours ago" -> an exact timestamp
function caughtAtFromHoursAgo(hoursAgo, now = Date.now()) {
  return now - Math.max(0, parseFloat(hoursAgo) || 0) * MS_PER_HOUR;
}

// x = hours since caught, measured live (extraHours lets the demo slider fast-forward)
function hoursSince(timestamp, extraHours = 0, now = Date.now()) {
  return Math.max(0, (now - timestamp) / MS_PER_HOUR + extraHours);
}

// The score of a saved catch at any moment: score(x) = b * e^(-m * x)
function liveStatus(catchRecord, extraHours = 0, now = Date.now()) {
  const x = hoursSince(catchRecord.caughtAt, extraHours, now);
  const score = catchRecord.b * Math.exp(-catchRecord.m * x);
  const cutoff = MODEL2_DATA.safe_cutoff;
  const left = catchRecord.b <= cutoff ? 0 : Math.max(0, Math.log(catchRecord.b / cutoff) / catchRecord.m - x);
  return { x, score, hoursLeft: left, stage: stageFor(score) };
}

// "7.8" hours -> "7 h 48 min"
function formatHours(h) {
  if (h <= 0) return "0 min";
  if (h >= 48) { const d = Math.floor(h / 24), rest = Math.round(h % 24); return rest ? `${d} days ${rest} h` : `${d} days`; }
  const totalMin = Math.round(h * 60), hrs = Math.floor(totalMin / 60), min = totalMin % 60;
  return hrs > 0 ? `${hrs} h ${min} min` : `${min} min`;
}

if (typeof module !== "undefined") module.exports = { runModel2, lookupFish, predictM, initialScore, stageFor,
  caughtAtFromHoursAgo, hoursSince, liveStatus, formatHours };
