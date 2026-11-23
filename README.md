Last Catch 🐟

Our mission is that no catch goes to waste. A freshness tool that helps small-scale fishers sell their catch before it spoils and send what can't be eaten to by-product uses instead of the dump.

The problem

Many small-scale fishers in rural areas have no ice or cold storage. Catch that doesn't sell within hours spoils and gets thrown away, which wastes food and fishers' income. Fishers and buyers rarely have a clear way to know how long a catch will stay safe to sell.

What it does
A seller enters the fish type, weight, whether it's on ice, hours since caught, and a short description (max 100 characters), such as "gutted on the boat, kept in cooler, hot day, few bruised."
Model 1 reads the description and gives it a score from 0 to 10 and passes through other features such as type, weight, and whether or not the catch was stored on ice.
Model 2 uses machine learning to predict how fast that specific catch will spoil.
The seller sees a freshness score out of 100, a color (green → yellow → orange → red → grey), and how many hours it stays food-safe.
Posted catches are tracked live from the time they were caught. Their scores drop in real time, and they're saved in the browser.
Once a catch drops below the food-safe line, it turns grey: by-product only (compost, fertilizer or bait), so it's never sold as food and never simply dumped.
How it works
Model 1: description → score (model1/model1.js)
Stores the seller's input in variables: fish type (string), weight (number), stored in ice (true/false), description (text).
Scores the description from 0 to 10, starting at 5 (neutral):
Good signs raise it (gutted, bled, ice slurry, firm, clear eyes…)
Bad signs lower it (bruised, crushed, hot day, caught yesterday…)
Danger signs set it to 0 and force grey (sewage outfall, red tide, rotten, chemical…)
Handles negation, so "no damage" isn't counted as damage and "no sewage nearby" doesn't trigger danger.
Runs in the browser with no API key and no internet.
Model 2: machine learning spoilage model (model2/)
Fish catalog: 116 commonly caught species, with a focus on rural areas, grouped into 9 spoilage groups (lean white fish, oily fish, tuna/mackerel family, sharks and rays, freshwater, crustaceans, bivalves, squid/octopus, abalone/whelks), plus a fat level for each fish.
b (starting score) comes from Model 1: b = 75 + 2.5 × description score (0 if a danger sign was found).
m (spoilage rate) is predicted by a scikit-learn linear regression from fish group, fat level, ice, description score and weight.
Freshness over time: score(x) = b · e^(−m·x), where x is hours since caught. Spoilage speeds up as bacteria multiply, so the score follows a curve. In log form it is a straight line: ln(score) = ln(b) − m·x.
Results on a held-out test set: R² = 0.988, with a median error of about 8% in predicted food-safe hours.
Trained in Python (train_model2.py). The learned weights are exported to model2_data.js and run in the browser.

Honest note on data: Model 2 is trained on synthetic data generated from placeholder shelf-life estimates for each fish group. These numbers still need to be checked against food-science sources, and the test results measure how well the model learns that data, not real-world accuracy. A real deployment would retrain on fishers' logged outcomes (sold fresh vs. spoiled). Freshness scores are guidance, not a food-safety certificate.

Time tracking

When a catch is posted, the app saves the exact time it was caught and recalculates the score every 30 seconds. A demo fast-forward slider shows how catches lose freshness over 48 hours.

The waste problem we targeted

We targeted post-harvest fish loss among small-scale fishers without cold storage, where unsold catch spoils within hours and is thrown away. Last Catch predicts how long each catch stays food-safe, so fishers know how urgently to sell it, and it routes anything past the food-safe point to by-product uses instead of the dump. We would measure success by comparing the kilograms of catch sold or reused against the kilograms reported discarded, per fisher, per month.

Files
index.html               the website
model1/model1.js         Model 1: description score
model2/fish_catalog.py   116 fish + spoilage groups
model2/train_model2.py   trains Model 2 (Python, scikit-learn)
model2/model2_data.js    trained weights used by the website
model2/model2.js         runs Model 2 + live time tracking in the browser

To retrain: pip install numpy scikit-learn, then cd model2 && python3 train_model2.py.

What's next
Buyer map showing nearby catches as colored dots, with matching and messaging between buyers and sellers
A shared online database so buyers on other phones can see catches
Retrain Model 2 on real fishers' data
SMS / WhatsApp access for fishers without mobile data
Spelling-tolerant input (fuzzy matching) and local languages (isiXhosa, Afrikaans)
