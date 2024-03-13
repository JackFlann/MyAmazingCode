from flask import Flask, render_template, request,jsonify
import openai
import requests

app = Flask(__name__)
openai.api_key = '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'

# Earnings code
def show_earnings(symbol):
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey=M6MP1BDPRRJJ7Q18"
    r = requests.get(url)
    data = r.json()
    return data

def analyze_earnings(symbol):
    earnings_data = show_earnings(symbol.upper())
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[
                                                {"role": "system", "content": "Analyze this stocks earnings data if its a smart investment.Break the analysis up into sections"},
                                                {"role": "user", "content": str(earnings_data)}
                                            ],
                                            max_tokens=700)
    return response['choices'][0]['message']['content'].strip()

# Company overview code
def show_company_overview(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey=MR18U5N60WGN89QU"
    r = requests.get(url)
    data = r.json()
    return data

def analyze_company(symbol):
    overview_data = show_company_overview(symbol.upper())
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[
                                                {"role": "system", "content": "Analyze this company overview data if its a smart investment and doing good things.Break the analyses up into sections"},
                                                {"role": "user", "content": str(overview_data)}
                                            ],
                                            max_tokens=700)
    return response['choices'][0]['message']['content'].strip()

# Market performance code
def show_market_performance(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey=OYW1F6RZ2YLJMY4X"
    r = requests.get(url)
    data = r.json()
    return data

def analyze_market(symbol):
    market_data = show_market_performance(symbol.upper())
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[
                                                {"role": "system", "content": "Analyze this market performance data and how its doing in the stock market today and if its a good investment decision.Break your analysis up into sections"},
                                                {"role": "user", "content": str(market_data)}
                                            ],
                                            max_tokens=700)
    return response['choices'][0]['message']['content'].strip()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form['symbol']
        analysis_type = request.form['analysis_type']
        
        if analysis_type == 'earnings':
            result = analyze_earnings(symbol)
        elif analysis_type == 'company':
            result = analyze_company(symbol)
        elif analysis_type == 'market':
            result = analyze_market(symbol)
        else:
            result = "Invalid analysis type"
        
        return render_template('result.html', result=result)
    
    return render_template('index.html')





@app.route('/home', methods=['GET'])

def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345, debug=True)
