import os
import requests
from dotenv import load_dotenv
import time
import json

load_dotenv()

api_key = os.environ.get("G_API_KEY")
cse_id = os.environ.get("CSE_ID")

titles = [
    "The Intelligent Investor",
    "A Random Walk Down Wall Street",
    "One Up On Wall Street",
    "Common Stocks and Uncommon Profits",
    "The Little Book of Common Sense Investing",
    "Rich Dad Poor Dad",
    "The Millionaire Next Door",
    "The Essays of Warren Buffett",
    "You Can Be a Stock Market Genius",
    "The Little Book That Still Beats the Market",
    "Principles: Life and Work",
    "Your Money or Your Life",
    "Financial Freedom",
    "The Only Investment Guide Youll Ever Need",
    "I Will Teach You to Be Rich",
    "The Bogleheads' Guide to Investing",
    "The Dhandho Investor",
    "Market Wizards",
    "Thinking, Fast and Slow",
    "Antifragile: Things That Gain from Disorder",
    "Invested",
    "The Little Book That Builds Wealth",
    "The Psychology of Money",
    "The Simple Path to Wealth",
    "Unshakeable",
    "Stocks to Riches",
    "Bulls, Bears and Other Beasts",
    "Coffee Can Investing",
    "Lets Talk Money",
    "Graham and Doddsville: A Journey Through Value Investing",
    "The Thoughtful Investor",
    "How to Avoid Loss and Earn Consistently in the Stock Market",
    "The Equity Culture: The Story of the Indian Stock Market",
    "Value Investing and Behavioral Finance",
    "The Little Book of Value Investing",
    "The Financial Independence Marathon",
    "Indian Share Market for Beginners",
    "The Everything Guide to Investing in Your 20s & 30s",
    "The Dhando Investor",
    "The Indian Mutual Fund Handbook",
    "The Little Book of Behavioral Investing",
    "The Winning Investment Habits of Warren Buffett & George Soros",
    "The Art of Value Investing",
    "The Mind of a Trader",
    "The Richest Engineer",
    "Investing in India",
    "Warren Buffett and the Interpretation of Financial Statements",
    "Mastering the Art of Stock Investing",
    "Mutual Funds for Dummies",
    "The Indian Financial System: Markets, Institutions and Services",
    "Cryptoassets: The Innovative Investor's Guide to Bitcoin and Beyond",
    "Mastering Bitcoin: Unlocking Digital Cryptocurrencies",
    "Bitcoin Billionaires: A True Story of Genius, Betrayal, and Redemption",
    "The Bitcoin Standard: The Decentralized Alternative to Central Banking",
    "Crypto Trading Strategies for Beginners",
    "Cryptocurrency: How Bitcoin and Digital Money are Challenging the Global Economic Order",
    "Blockchain Basics: A Non-Technical Introduction in 25 Steps",
    "The Basics of Bitcoins and Blockchains",
    "Cryptoassets: The Guide to Bitcoin, Blockchain, and Cryptocurrency for Investment Professionals",
    "Bitcoin and Cryptocurrency Technologies",
    "Cryptocurrency Investing For Dummies",
    "Digital Gold: Bitcoin and the Inside Story of the Misfits and Millionaires Trying to Reinvent Money",
    "The Age of Cryptocurrency: How Bitcoin and Digital Money are Challenging the Global Economic Order",
    "Mastering Ethereum: Building Smart Contracts and DApps",
    "Bitcoin for the Befuddled",
    "The Truth About Crypto: A Practical, Easy-to-Understand Guide to Bitcoin, Blockchain, NFTs, and Other Digital Assets",
    "The Internet of Money",
    "Cryptocurrency Mining For Dummies",
    "DeFi and the Future of Finance",
    "Bitcoin Money: A Tale of Bitville Discovering Good Money",
    "The Blocksize War: The Battle Over Who Controls Bitcoins Protocol Rules",
    "Crypto Trading 101: How to Buy, Sell, and Trade Cryptocurrencies",
    "Token Economy: How the Web3 reinvents the Internet",
    "Cryptoassets: The Innovative Investor's Guide to Bitcoin and Beyond",
    "The Crypto Trader: How anyone can make money trading Bitcoin and other cryptocurrencies",
    "The 4-Hour Workweek: Escape 9-5, Live Anywhere, and Join the New Rich",
    "Passive Income, Aggressive Retirement",
    "Rental Property Investing: How to Create Wealth and Passive Income Through Smart Buy & Hold Real Estate Investing",
    "The Book on Rental Property Investing",
    "The Book on Managing Rental Properties",
    "The Ultimate Guide to Real Estate Investment in India",
    "Dividend Growth Machine: How to Supercharge Your Investment Returns with Dividend Stocks",
    "Your Complete Guide to Factor-Based Investing",
    "Create Multiple Streams of Income",
    "The Wealthy Gardener: Lessons on Prosperity Between Father and Son",
    "Real Estate Investing For Dummies",
    "Money: Master the Game",
    "Retire Young Retire Rich: How to Get Rich Quickly and Stay Rich Forever!"
    "The Lazy Investor's Guide to Real Estate Investing",
    "Financial Freedom with Real Estate Investing",
    "The Automatic Millionaire: A Powerful One-Step Plan to Live and Finish Rich",
    "Investing in Real Estate Private Equity",
    "Passive Income: 25 Proven Business Models",
    "Making Money Out of Property in South Africa",
    "The Wealth Chef: Recipes to Make Your Money Work Hard, So You Dont Have To",
    "How to Make Money in Real Estate",
    "The Money Tree: A Story About Finding the Fortune in Your Own Backyard",
    "Financial Freedom: A Proven Path to All the Money You Will Ever Need",
    "The Passive Income Playbook",
    "Rich Dads Guide to Investing",
]


def google_search(query, api_key, cse_id, num_results=1):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": api_key, "cx": cse_id, "num": num_results}
    response = requests.get(url, params=params)
    results = response.json().get("items", [])
    return results[0]["link"]


def get_pdfs():
    if not os.path.exists('./pdfs'):
        os.mkdir('pdfs')
    remaining_titles = []
    for title in titles:
        query = f"{title} book free pdf download"
        link = google_search(query, api_key, cse_id)
        if ".pdf" in link:
            os.system(f"wget {link} -O ./pdfs/{title.replace(' ', '_')}.pdf")
        else:
            remaining_titles.append(title)
        time.sleep(5)
    with open("remaining_titles.json", "w") as file:
        json.dump({"remaining_titles": remaining_titles}, file)
    return remaining_titles

if __name__ == "__main__":
    get_pdfs()
