# The "Sugar Trap" Market Gap Analysis

## A. Executive Summary

Analysis of 134,218 cleaned Open Food Facts products found that only 30.2% (40,546 products) fall into snack-relevant categories, and within those, just 8.9% currently combine high protein (10g+ per 100g) with low sugar (under 5g per 100g). The biggest gap is in **Chocolate & Confectionery**, where only 192 of 7,135 products (2.7%) meet that profile despite the category being one of the largest and most sugar-saturated in the dataset. This points to a genuine "Blue Ocean" opportunity for a high-protein, low-sugar confectionery product, an area current manufacturers have largely left unaddressed. A brand-concentration check ("Who Owns This Shelf?") further shows this specific niche is not yet dominated by major players, lowering the barrier for a new entrant.

## B. Project Links

- **Link to Notebook:** https://colab.research.google.com/drive/1Wk3fg2JzlL4k7pu87EPqKdFkPYlVcI0v?usp=sharing
- **Link to Dashboard:** https://amalitech-deg-project-based-challenges-v9lvlazrpt65pkffazgjwj.streamlit.app/
- **Link to Presentation:** https://drive.google.com/file/d/1_ys4PLifmEaccboD2ZDah-xqsrpY1Wse/view?usp=drive_link

## C. Technical Explanation

### Data Cleaning

Rather than downloading Open Food Facts' full multi-gigabyte export, the notebook streams the compressed `.csv.gz` file directly in chunks, filtering for usable rows as it goes rather than after the fact. Of 1,400,000 raw rows scanned, only 154,839 (11.1%) had complete `product_name`, `sugars_100g`, `proteins_100g`, and `categories_tags` fields — rows missing any of these were dropped rather than imputed, since fabricating central nutrition values would directly bias the sugar/protein gap analysis this project depends on. From there, biologically impossible values (any nutrient outside 0–100g per 100g of product) and "empty shell" entries (rows with 0.0g sugar, protein, *and* fat simultaneously — almost always incomplete submissions) were removed, dropping 3,659 rows. A final deduplication pass on `product_name` + `brands` + `categories_tags` removed 16,962 duplicate entries, leaving a final cleaned dataset of **134,218 unique products** (9.6% overall retention from the raw scan).

Category assignment (Story 2) parsed the comma-separated `categories_tags` column and mapped it to 6 high-level buckets (5 snack categories plus a "Non-Snack / Other" catch-all) using priority-ordered keyword matching, validated against real product samples rather than assumed correct from counts alone.

**Note on data hosting:** the cleaned dataset (`cleaned_snacks_data.csv`) is not committed to this repository per the submission guidelines. It is hosted externally and loaded by the dashboard at runtime via a direct URL.

### Candidate's Choice: "Who Owns This Shelf?"

A nutrition gap alone doesn't guarantee an easy market entry — if a handful of large brands already dominate a category, breaking in is a much harder fight than the nutrition chart alone suggests. This addition cross-references the identified opportunity category against the `brands` column already present in the cleaned dataset, surfacing the number of unique brands and the market share held by the top 3, with a plain-language read-out (fragmented / moderately concentrated / highly concentrated). This turns a purely nutritional finding into a more complete go/no-go signal for R&D — checking not just *whether* a gap exists, but *how contested* that gap already is — using data already collected, at no additional cost to the pipeline.

---
# Project Brief: The "Sugar Trap" Market Gap Analysis

**Client:** Helix CPG Partners (Strategic Food & Beverage Consultancy)
**Deliverable:** Interactive Dashboard, Code Notebook & Insight Presentation

---

## 1. Business Context

**Helix CPG Partners** advises major food manufacturers on new product development. Our newest client, a global snack manufacturer, wants to launch a "Healthy Snacking" line. They believe the market is oversaturated with sugary treats, but they lack the data to prove where the specific gaps are.

They have hired us to answer one question: **"Where is the 'Blue Ocean' in the snack aisle?"**

Specifically, they are looking for product categories that are currently under-served, areas where consumer demand for health (e.g., High Protein, High Fiber) is not being met by current product offerings (which are mostly High Sugar, High Fat).

## 2. The Data

You will use the **Open Food Facts** dataset, a free, open, and massive database of food products from around the world.

- **Source:** [Open Food Facts Data](https://world.openfoodfacts.org/data)
- **Format:** CSV (Comma Separated Values)
- **Warning:** The full dataset is massive (over 3GB). You are **not** expected to process the entire file. You should filter the data early or work with a manageable subset (e.g., the first 500,000 rows or specific categories).

## 3. Tooling Requirements

You have the flexibility to choose your development environment:

- **Option A (Recommended):** Use a cloud-hosted notebook like **Google Colab**, or **Deepnote**, etc.
- **Option B:** Use a local **Jupyter Notebook** or **VS Code**.
  - _Condition:_ If you choose this, you must ensure your code is reproducible. Do not reference local file paths (e.g., `C:/Downloads/...`). Assume the dataset is in the same folder as your notebook.
- **Dashboarding:** The final output must be a **publicly accessible link** (e.g., Tableau Public, Google Looker Studio, Streamlit Cloud, or PowerBI Web).

---

## 4. User Stories & Acceptance Criteria

### Story 1: Data Ingestion & "The Clean Up"

**As a** Strategy Director,
**I want** a clean dataset that removes products with erroneous nutritional information,
**So that** my analysis is not skewed by bad data entry.

- **Acceptance Criteria:**
  - Handle missing values: Decide what to do with rows that have `null` or empty `sugars_100g`, `proteins_100g`, or `product_name`.
  - Handle outliers: Filter out biologically impossible values.
  - **Deliverable:** A cleaned Pandas DataFrame or SQL table export.

### Story 2: The Category Wrangler

**As a** Product Manager,
**I want** to group products into readable high-level categories,
**So that** I don't have to look at 10,000 unique, messy tags like `en:chocolate-chip-cookies-with-nuts`.

- **Acceptance Criteria:**
  - The `categories_tags` column is a comma-separated string (e.g., `en:snacks, en:sweet-snacks, en:biscuits`). You must parse this string.
  - Create a logic to assign a "Primary Category" to each product based on keywords.
  - Create at least 5 distinct high-level buckets.

### Story 3: The "Nutrient Matrix" Visualization

**As a** Marketing Lead,
**I want** to see a Scatter Plot comparing Sugar (X-axis) vs. Protein (Y-axis) for different categories,
**So that** I can visually spot where the products are clustered.

- **Acceptance Criteria:**
  - Create a dashboard (PowerBI, Tableau, Streamlit, or Python-based charts) displaying this relationship.
  - Allow the user to filter the chart by the "High Level Categories" you created in Story 2.
  - **Key Visual:** Identify the "Empty Quadrant" (e.g., High Protein + Low Sugar).

### Story 4: The Recommendation

**As a** Client,
**I want** a clear text recommendation on what product we should build,
**So that** I can take this to the R&D team.

- **Acceptance Criteria:**
  - On the dashboard, include a "Key Insight" box.
  - Complete this sentence: _"Based on the data, the biggest market opportunity is in [Category Name], specifically targeting products with [X]g of protein and less than [Y]g of sugar."_

---

## 5. Bonus User Story: The "Hidden Gem"

**As a** Health Conscious Consumer,
**I want** to know which specific ingredients are driving the high protein content in the "good" products,
**So that** I can replicate this in our new recipe.

- **Acceptance Criteria:**
  - Analyze the `ingredients_text` column for products in your "High Protein" cluster.
  - Extract and list the Top 3 most common protein sources (e.g., "Whey", "Peanuts", "Soy").

---

## 6. The "Candidate's Choice" Challenge

**As a** Creative Analyst,
**I want** to add one additional feature or analysis to this project that I believe provides massive value,
**So that** I can show off my business acumen.

- **Instructions:**
  - Add one more chart, filter, or metric that wasn't asked for.
  - Explain **why** you added it.
  - **There is no wrong answer, but you must justify your choice.**

---

## 7. Submission Guidelines

Please edit this `README.md` file in your forked repository to include the following three sections at the top:

### A. The Executive Summary

- A 3-5 sentence summary of your findings.

### B. Project Links

- **Link to Notebook:** (e.g., Google Colab, etc.). _Ensure sharing permissions are set to "Anyone with the link can view"._
- **Link to Dashboard:** (e.g., Tableau Public / Power BI Web, etc.).
- **Link to Presentation:** A link to a short slide deck (PDF, PPT) AND (Optional) a 2-minute video walkthrough (YouTube) explaining your results.

### C. Technical Explanation

- Briefly explain how you handled the "Data Cleaning".
- Explain your "Candidate's Choice" addition.

**Important Note on Code Submission:**

- Upload your `.ipynb` notebook file to the repo.
- **Crucial:** Also upload an **HTML or PDF export** of your notebook so we can see your charts even if GitHub fails to render the notebook code.
- Once you are ready, please fill out the [Official Submission Form Here](https://forms.cloud.microsoft/e/CeQN2mCyUr) with your links

---

## 🛑 CRITICAL: Pre-Submission Checklist

**Before you submit your form, you MUST complete this checklist.**

> ⚠️ **WARNING:** If you miss any of these items, your submission will be flagged as "Incomplete" and you will **NOT** be invited to an interview.
>
> **We do not accept "permission error" excuses. Test your links in Incognito Mode.**

### 1. Repository & Code Checks

- [ ] **My GitHub Repo is Public.** (Open the link in a Private/Incognito window to verify).
- [ ] **I have uploaded the `.ipynb` notebook file.**
- [ ] **I have ALSO uploaded an HTML or PDF export** of the notebook.
- [ ] **I have NOT uploaded the massive raw dataset.** (Use `.gitignore` or just don't commit the CSV).
- [ ] **My code uses Relative Paths.**

### 2. Deliverable Checks

- [ ] **My Dashboard link is publicly accessible.** (No login required).
- [ ] **My Presentation link is publicly accessible.** (Permissions set to "Anyone with the link can view").
- [ ] **I have updated this `README.md` file** with my Executive Summary and technical notes.

### 3. Completeness

- [ ] I have completed **User Stories 1-4**.
- [ ] I have completed the **"Candidate's Choice"** challenge and explained it in the README.

**✅ Only when you have checked every box above, proceed to the submission form.**

---
