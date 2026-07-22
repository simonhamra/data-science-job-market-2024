# AD-688 Team 4: Data Science & Business Analytics Trends in 2024

A team project analyzing the 2024 job market for data, BI and machine-learning roles, built as a Quarto site from the Lightcast job-postings dataset. We look at the most in-demand skills, how much AI/ML is reshaping the field, where the skill gaps are, and what the pay and geography look like.

**Live site: https://simonhamra.github.io/AD-688---Team-4---Project/**

## What's on the site

The site is split into sections, each answering one question about the market:

- **Data Analysis** and **Exploratory Analysis**, cleaning the postings and finding the broad trends
- **Skill Gap Analysis**, what's in demand vs what candidates actually have
- **Advanced Visualizations**, the deeper charts
- **Text Mining & Classification** (my part, see below)
- **KMeans Clustering Analysis**, grouping roles by their skill profiles

## My part: Text Mining & Classification

I owned this whole section. The task from the brief was "use classification to detect whether a role requires ML/Data Science using structured features." But before writing any model I looked at the data, and it changed the question.

**The surprise.** The file looks like it has ~13 million lines, but that's a trap: the job-description field has line breaks inside the text, so it's counting paragraphs. Parsed properly there are **72,454 real postings**. Then I checked the occupation codes and every single row is the same one: Business Intelligence Analyst. The dataset is already one occupation captured across thousands of companies. So "classify the occupation" is impossible, there's only one class.

So I reframed it into something answerable and honestly more interesting: **within these BI roles, which ones are genuinely ML/data-science jobs underneath, and which are the traditional reporting-and-dashboards kind?** Same title on the door, two different jobs.

**Defining the target without cheating.** I label a posting ML/DS-intensive if its skills list a genuine ML/DS skill (Machine Learning, Data Science, Deep Learning, NLP, TensorFlow...). I deliberately do **not** count Python, R or SQL, because they're near-universal analyst tools. An earlier version that counted them tagged 59% of the positive class on the word "Python" alone and made the two groups look identical. Restricting to real ML/DS skills gives a clean split: about **20% ML/DS-intensive** (14,569 postings) vs 80% traditional BI (57,885).

**The leakage problem, and how I handled it.** My label is built from the skill list, so I had to be careful. Two traps:

- Feed the model the skills that define the label, and it hits ~0.98 AUC by just spotting "Machine Learning" in the text. That's circular and worthless.
- Throw away all skills and use only metadata (pay, education, experience, location), and it drops to ~0.63 AUC, barely above a coin flip.

So I took the middle path: I removed every label-defining skill (40 of them), then let the model use the remaining 120 structured skills plus job metadata. The model never sees the words that define the label, but it can still read the company a role keeps: ML/DS roles co-list AWS, Spark-adjacent tooling and statistics, while traditional BI roles co-list SAP, Excel and reporting suites. That's honest signal, not memorisation.

**Results.** Two models on the held-out test set (149 features, no label-defining skills, no raw text):

| Model | Accuracy | F1 | ROC-AUC |
|-------|:--------:|:--:|:-------:|
| Random Forest | 0.887 | 0.741 | 0.938 |
| Keras MLP (main model) | 0.855 | 0.704 | 0.930 |

They finish in a near dead heat around **0.93 AUC**, way above the 0.63 I got from metadata alone, and above the 0.5 coin-flip line. The features that matter most are the co-listed non-defining skills (cloud, data-engineering, statistics tooling) alongside advertised salary and required education. I also ran a Naive Bayes on the raw text as the optional extra-credit model: it scores higher, but only because the descriptions literally spell out "machine learning", so I included it on purpose to show the exact circularity I controlled for.

**What it means for a job seeker.** If you're aiming for the data-science end of this market, the rest of a posting gives the role away before you even reach the headline skills. A higher salary band + a master's requirement + cloud/big-data/stats tooling usually means it's a real ML job wearing a "BI Analyst" title. If it asks for a bachelor's and lists Excel, SAP and Power BI, expect dashboards, not models.

Read the full write-up with all the charts here: https://simonhamra.github.io/AD-688---Team-4---Project/text_mining_classification.html

## Team

Built by Team 4: Simon Hamra, Meera Chaddha, Miao Liu, Keiper (keiperla). Each of us owned different sections of the analysis.

## Tech stack

Quarto, Python, pandas, scikit-learn, TensorFlow / Keras, plotly, TF-IDF (scikit-learn), matplotlib / wordcloud. Site deployed via GitHub Pages.

## Running it locally

The job-postings CSV isn't in the repo (it's over GitHub's 100mb limit). Download it into `/data` from [this link](https://drive.google.com/file/d/1V2GCHGt2dkFGqVBeoUFckU4IhUgk4ocQ/view), then:

```bash
# edit the .qmd files, then push
git add . && git commit -m "your message" && git push origin main

# publish to the live site
quarto publish gh-pages
```
