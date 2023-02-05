# Breaking-News-Trends-Detection
# Trend Detection in News

The goal of this project is to develop a solution for the automatic detection of trends in news (breaking news) using Twitter, the News API (https://newsapi.org/) and scraping of online newspapers (choose two or more newspapers). 

The solution should run automatically several times a day (set the frequency) and should allow:
- Finding a general trend (using the three sources) - implement a simple algorithm (e.g., word count)
- Comparing the three sources, are there any noticeable differences (e.g., more "political" news in newspapers, news always comes out first on Twitter and then in newspapers...)
- Visualize the evolution of trends over time.

In the final deliverable, at least one week of data should be used for analysis and discussed. The results of these analyses will be visualized on a static web page. There are no constraints on the solution/technology to be used.

## Objectives
### Data Acquisition
- Know how to use a RESTful API or a stream API
- Know how to configure a crawler/scraper capable of analyzing multiple pages (using a distributed approach)
- Filter and aggregate different types of data (structured, semi-structured, unstructured)
- Implement a simple data analysis/visualization
- The application should be designed to be "distributed"

### Infrastructure
- Automate the deployment of an application and its database
- The web server is scalable (replicated)

### Data Acquisition Constraints
- Use the Twitter API to find a current topic
  - Use appropriate filters
  - Can parallelize using 2 different accounts
- Use scraping to find news in an online newspaper/blog... Here, the goal is to give a starting URL and then create a crawler/spider capable of traversing different URLs in the given page (following certain rules)
  - Idea: create a list of URLs to explore and dispatch to different actors in the infrastructure
- Use a second API (https://newsapi.org/).
- The collected data will be stored in a database for analysis
- A simple analysis + evaluation should be implemented and visualized in a static HTML page

### Infrastructure Constraints
- Deploy everything with Kubernetes
  - The application
  - The database
  - The web server
- Build the data acquisition application stateless
  - It should also work in multiple replicas
  - Replicas can stop and restart at any time
- Store the data in the database
  - Persistent state of the application
- The web server should be replicated
  - Replicas can stop and restart at any time
  - Web servers serve the same web page, result of the app

