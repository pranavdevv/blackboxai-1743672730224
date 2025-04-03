import requests
from bs4 import BeautifulSoup
import sqlite3
import json
from urllib.parse import urljoin

class QuestionScraper:
    def __init__(self):
        self.base_urls = {
            'leetcode': 'https://leetcode.com/problems/',
            'geeksforgeeks': 'https://www.geeksforgeeks.org/',
            'hackerrank': 'https://www.hackerrank.com/challenges/'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.conn = sqlite3.connect('coding_contest.db')
        
    def scrape_leetcode(self, problem_url):
        try:
            response = requests.get(urljoin(self.base_urls['leetcode'], problem_url), 
                                  headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract question details
            title = soup.find('div', {'data-cy': 'question-title'}).text
            description = soup.find('div', {'class': 'content__u3I1'}).text
            difficulty = soup.find('div', {'diff': True}).text
            
            return {
                'title': title,
                'description': description,
                'difficulty': difficulty,
                'source': 'leetcode'
            }
        except Exception as e:
            print(f"Error scraping LeetCode: {e}")
            return None

    def scrape_geeksforgeeks(self, problem_url):
        try:
            response = requests.get(urljoin(self.base_urls['geeksforgeeks'], problem_url),
                                  headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract question details
            title = soup.find('h1', {'class': 'title'}).text
            description = soup.find('div', {'class': 'problems_problem_content__Xm_eO'}).text
            difficulty = soup.find('span', {'class': 'difficulty'}).text
            
            return {
                'title': title,
                'description': description,
                'difficulty': difficulty,
                'source': 'geeksforgeeks'
            }
        except Exception as e:
            print(f"Error scraping GeeksforGeeks: {e}")
            return None

    def save_question(self, question_data):
        c = self.conn.cursor()
        c.execute('''INSERT INTO questions 
                    (title, description, difficulty, time_limit)
                    VALUES (?, ?, ?, ?)''',
                 (question_data['title'],
                  question_data['description'],
                  question_data['difficulty'],
                  self.get_time_limit(question_data['difficulty'])))
        question_id = c.lastrowid
        
        # Save test cases (example implementation)
        c.execute('''INSERT INTO test_cases
                    (question_id, input, expected_output, is_hidden)
                    VALUES (?, ?, ?, ?)''',
                 (question_id, 'Sample Input', 'Sample Output', False))
        
        self.conn.commit()
        return question_id

    def get_time_limit(self, difficulty):
        limits = {
            'Easy': 10,
            'Medium': 20,
            'Hard': 30
        }
        return limits.get(difficulty, 15)

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    scraper = QuestionScraper()
    # Example usage:
    # leetcode_question = scraper.scrape_leetcode('two-sum')
    # if leetcode_question:
    #     scraper.save_question(leetcode_question)
    scraper.close()