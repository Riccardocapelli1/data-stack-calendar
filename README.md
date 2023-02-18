# Summary
A modern data stack wall aggregating events and conferences from Twitter for data engineers, analytics engineers and data analyst.

This code helps you to visualize selected tweets that contain different keywords from profile names of your Twitter Dev account using Twitter's official API Tweepy. This code requires API keys and secrets to use Tweepy's functionality. The user can replace their API keys and secrets by adding the secret name and the secret key in the Github settings.

## Requirements
This code requires pip packages to execute the functionality and you will find them in the file /.github/workflows/static.yml.\
The deployment action installs the required libraries in a container by using pip install command.

## API
This code requires access to Twitter's official API Tweepy. The user must have API keys and secrets to use Tweepy's functionality. The user can replace their API keys and secrets provided by the Twitter Dev account by adding the to the security settings in Github.

## Functionality
This code is used to download the tweets related to different keywords and profile names from Twitter using Twitter's official API Tweepy. The user needs to provide the profile names and keywords they want to download the tweets from. The code then downloads the tweets and stores them in a pandas dataframe.

The code then maps the profile names with the official website and twitter profile page. It filters the tweets that contain the keywords mentioned in the code.

The code then creates different dataframes based on the tweets that contain the keywords "Conference|Summit", "Certification|Courses|Training", and the other generical keywords "Blog|Event|Podcast|Webinar".

The code then filters the dataframes for the tweets that contain the specified keywords and the created date is greater than or equal to the first day of the previous month.

Finally, the code writes the HTML pages to display the tweets and the filtered dataframes data summary and daily visit count to CSV files.

## Limitation
The Twitter API has a limit on the number of requests you can make in a given time period. This code is designed to wait when the rate limit is reached, but the user may need to wait for the rate limit to reset before they can use the API again.

## How to Run
To run the code, download the code and replace your API keys and secrets with the current keys and secrets. After creating the keys create a deployment action to Github pages. The code will create HTML files with the filtered tweets. You can personalize the tweets keys to filter to adapt the content you wish to select.\

## References
This code is based on the Tweepy library and the CountAPI.

    Tweepy: http://www.tweepy.org/

    CountAPI: https://countapi.xyz/

## License
This project is licensed under the MIT License.

## Author
This code is written by Riccardo Capelli and ChatGpt, to help the data and analytics community discover conference, course and generic information from the modern-data-stack.

See the output at:\
https://riccardocapelli1.github.io/data-stack-wall
