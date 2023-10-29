from flask import Flask, jsonify, request
from flask_cors import CORS
from facebook_scraper import get_posts, get_profile
import numpy as np
from linkedin import scrape_linkedin
from sentiment_analysis_P2 import nb_ratio
import pandas as pd
from truth_estimate import assess_truthfulness
from clip import check_answer, analyze_about
import random

app = Flask(__name__)
CORS(app)

linkedin = None
facebook = None
questions = None
answers = None
popularity_score = None
about = None
sentiment_value = None
truthfulness = None


# candidate route
# goes to the candidate __package__

# recruiter route

def sigmoid(x):
	return 1 / (1 + np.exp(-x))


def process_github(handle):
	pass


def process_facebook(handle):
	likes = []
	post_texts = []
	truth_scores = []
	num_posts = 0
	for post in get_posts(handle, pages=2, credentials=("vaibhavagrawal1510", "guliya999208")):
		# for key in post.keys():
		#     print(key)
		print(f"processed a post!")
		likes.append(post["likes"])
		post_texts.append(post["text"])
		truth_scores.append(assess_truthfulness(post["text"]))
		num_posts += 1
		if num_posts == 5:
			break
	

	truthfulness = sigmoid(np.sum(np.array(truth_scores))) * 100.0 # percent
	if len(likes) == 0:
		return 0, 0, 0

	popularity_score = sigmoid(np.sum(np.array(likes)) / len(likes) * 15 + len(likes)) * 100
	custom_tweets = pd.DataFrame({"tweet": post_texts})
	sentiment_value = nb_ratio(custom_tweets)
	return popularity_score, sentiment_value, truthfulness


def process_linkedin(link):
	about = scrape_linkedin(link)
	about = about.split(" ")
	return about



@app.route("/candidate", methods=["POST"])
def process_candidate_input():
	global linkedin
	global facebook
	global answers
	global popularity_score
	global sentiment_value
	global truthfulness
	global about

	body = request.json
	linkedin = body["linkedin"]
	print(f"THE LINKEDIN LINK IS {linkedin}")
	facebook = body["facebook"]
	print(f"THE FACEBOOK LINK IS {facebook}")
	answers_mcq = body["answers_mcq"]
	answers = body["answers"]

	print(answers_mcq)
	answers_mcq = np.array(answers_mcq)
	answers_mcq *= 20 + random.randint(0, 10)

	result = check_answer(answers)	

	if result == 0:
		result = "According to the subjective test, the candidate has a practical approach in tough situations."

	elif result == 1:
		result = "According to the subjective test, the candidate might not be very good at handling tough situations, but with practice he could learn."
	else:
		result = "According to the subjective test, the candidate is not able to handle high pressure situations, and this might be a hindrance to his overall performance."

	popularity_score, sentiment_value, truthfulness = process_facebook(facebook)
	print(f"DONE PROCESSING FACEBOOK")
	about = process_linkedin(linkedin)
	about = about[:70]
	about = " ".join(about)
	# print(about)
	# print(result)
	# print(answers_mcq)
	professions = analyze_about(about)
	print(professions.tolist())

	# popularity_score = 0
	# sentiment_value = 0
	# truthfulness = 0


	professions = professions.tolist()
	professions = [str(prof) for prof in professions]

	return {"popularity_score": popularity_score, "sentiment_value": sentiment_value, "about": about, "result": result, "truthfulness": truthfulness, "answers_mcq": answers_mcq.tolist(), "professions": professions}


# @app.route("/recruiter", methods=["POST"])
# def return_processed_values():
# 	global linkedin
# 	global facebook
# 	global questions
# 	global answers
# 	global popularity_score
# 	global sentiment_value
# 	global truthfulness
# 	global about

# 	return {
# 		"about": about,
# 		"popularity": popularity_score,
# 		"sentiment": sentiment_value,
# 		"truthfulness": truthfulness,
# 	}

if __name__ == "__main__":
	# print(process_facebook("shubhankar.kamthankar"))

	app.run(host="10.2.130.139")
	# process_linkedin("https://www.linkedin.com/in/chaitanya100100/")


