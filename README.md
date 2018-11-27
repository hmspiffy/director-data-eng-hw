# Director of Data Engineering Homework

## Overview

Hi! In this homework, we will provide a bunch of data in S3, and we will ask you to model it in a useful way. The contents of the data are **ratings**, which are any number of basic interactions between two. For example, if I send a like to you, and then you see me pop up and decide to match with me, two ratings have occurred: the "like" rating and the "match" rating.

Ratings are some of the most important data we have at Hinge — everything from our recommendation engine to our product decisions to our lifecycle marketing campaigns to the effectivteness of our member services team depends on ratings being highly available and accurate. Hinge currently processes over a billion ratings a month, and one of the top priorities for an incoming data engineering lead would be to build a system that can handle the massive growth we expect to undergo in the coming years. 

First, we'll go into way too much detail about what these ratings are and how they interact, then we'll follow that up with the actual problem description as well as some considerations/gotchas. Have fun!

## Dataset Explanation
At Hinge, we track **ratings** between users. A rating is any of a number of actions that one user can take on another. 

We call the person sending the rating the **player** and the person receiving the rating the **subject**. On the app, there are a three main screens where players can send ratings to subjects:

1. The **Discover** screen, which is where a player can see a queue (one at the time) of subject profiles for the first time. On this screen the user can decide to apply one of the following actions:
	(1) Send a **like**.
	(2) Send a **like** with a **comment**.
	(3) **skip** a subject - In this case the player can see this subject again in the future. 
	(4) **remove** a subject - In case the player does not want to see this subject again in the future. 
	(5) **report** a subject - In case the player sees something inappropriate on the subject's profile, so the profile can be reviewed by our CS team.

2. The **Likes You** screen, where the player can review all of the people who have sent likes to them. On this screen, the player can:
	(1) **reject** the incoming like if she is not interested. 
	(2) **match** with the incoming like to start a chat 
	(3) **report** the incoming like to our CS team.

3. The **Chats** screen, where the player can chat with people with whom she has matched. On this screen, the only two ratings a player can send are:
	(1) **block** - remove the chat from the Chats screen for both users.
	(2) **report** - end the chat, as well as alert or CS team to look into it.

In this dataset, these ratings are represented by the following numbers:

| rating_type | meaning                           |
|-------------|-----------------------------------|
| 0           | skip                              |
| 1           | like                              |
| 2           | comment                           |
| 3           | remove/block/reject               |
| 4           | report                            |
| 5           | match                             |

 
### Rating Rules 
If a pair of users has either never interacted before, or only sent skips between themselves, they are able to perform any rating on each other, except match.

If a User A has sent a like to User B (`rating_type` 1 or 2), User A is unable to send another rating to User B until B responds. B is able to respond only with `rating_type` 3 to reject the incoming like, 4 to report User A for bad behavior, or 5 to match with User A and start chatting.

If User B responds with `rating_type` 5, the two users have matched, and they can start chatting. However, at any point, either of the two users may now send a `rating_type` of 3 to block/remove the other user or 4 to report the other for bad behavior.

If a pair of users has ever shared a `rating_type` of 3 or 4, those two users will forever be unable to access each other in the app, and no more ratings can be sent.

So an example series of ratings might look like this:

| timestamp           | player_id                        | subject_id                       | rating_type |
|---------------------|----------------------------------|----------------------------------|-------------|
| 2018-04-01 00:00:00 | 4a93b6ffc4f0bb16860ca385c8af511b | bb275bbc234a88043097fb9f7e56275a | 0           |
| 2018-04-01 01:00:00 | 4a93b6ffc4f0bb16860ca385c8af511b | bb275bbc234a88043097fb9f7e56275a | 0           |
| 2018-04-01 02:00:00 | 4a93b6ffc4f0bb16860ca385c8af511b | bb275bbc234a88043097fb9f7e56275a | 1           |
| 2018-04-01 03:00:00 | bb275bbc234a88043097fb9f7e56275a | 4a93b6ffc4f0bb16860ca385c8af511b | 5           |
| 2018-04-01 04:00:00 | 4a93b6ffc4f0bb16860ca385c8af511b | bb275bbc234a88043097fb9f7e56275a | 3           |

In this situation, User A skips User B a couple times before finally sending a like. User B reciprocates. User A then looks a little closer at the rest of User B’s photos and removes User B from his/her list of matches, and they never see each other again. 

I've also made a diagram in case that helps. Here, the rounded rectangles are screens in the app, and the circles are ratings that are available from certain screens. Ratings 3 and 4 are marked red as a reminder that they are terminal. Rating 0 is marked yellow as a reminder that it can be repeated any number of times by either user until a different kind of rating occurs.

![ratings](/ratings.svg)

The files in the S3 bucket have the same schema as in this example.

## The Homework
A month of fake ratings data are stored at s3://hinge-homework/director-data-engineering/ratings. We will be designing an ELT pipeline to make this stuff useful.

1. Spin up a database to store these ratings. As a reminder, Hinge uses Redshift, but feel free to use whatever is easiest for you.
2. Design a schema that easily enables analysis on this dataset. Write whatever code you need to write to actually transform the ratings data into your schema. Below we've included some sample analysis questions which may be helpful as reference.
3. Totally optional and not necessary extra credit: perform one of the below analyses on the dataset to show us how easy you made it, or show us something cool that you found yourself in the data.

In working on this homework, please work in a fork of this repo, and let us know when we can check out your code. We should be able to run your code with little difficulty. At Hinge, we use Bash and Python scripts to wrap these kinds of operations, but if you prefer something else, anything that we can run is fine. 

In the root directory of your fork, include a writeup justifying your ideas and methods. Consider how your method will scale and offer longer-term improvements. We don't expect your solution to hold up under stress, but we're very interested in your explanations of what will need to change for your solution to be productionized.

For this homework, we care most about wisdom in modeling the data and elegance in the methods of doing so. As the principal data engineer at Hinge, you will be setting the example for coding style and best practices.

#### Example questions for analysis, in order of increasing vagueness/realism:
* What is the average like rate (likes/(likes+skips))?
* What percentage of likes go unresponded to?
* What is the average reciprocation rate?
* What % of reports happen after two users connect as opposed to before?
* What is the average number of skips before a like?
* In discover, how often do people see duplicates subjects within a day (assume every subject is either skipped or liked)?
* How often do people change their mind about the people they like?

#### Some considerations:
* A single `rating_type` can have multiple semantic meanings. For example, a `rating_type` of 3 either means “Remove this person from the list of people I can send likes to”, “Reject this person’s incoming like”, or “Remove this person from my list of matches”, depending on the preceding ratings between a pair of users. It's important that your model be able to distingush between these different meanings.
* What if it were the case that every day, more files is added to this S3 bucket, and that you can’t even predict their exact names. How will you make sure that you will catch these and include them in your final model?
* What kinds of tests will you put in place to make sure that the final model is accurate? What about to ensure that the source data is accurate?
