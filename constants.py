import os
from langchain_community.document_loaders import CSVLoader, TextLoader, UnstructuredExcelLoader, Docx2txtLoader
from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredMarkdownLoader



ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
directory = "docs"
a = os.listdir(directory)
print(a)
# Define the folder for storing database
SOURCE_DIRECTORY = f"{ROOT_DIRECTORY}/SOURCE_DOCUMENTS"

PERSIST_DIRECTORY = f"{ROOT_DIRECTORY}/DB"

MODELS_PATH = "./models"

# Can be changed to a specific number
INGEST_THREADS = min(os.cpu_count(),8)

DOCUMENT_MAP = {
    ".txt": TextLoader,
    ".md": UnstructuredMarkdownLoader,
    ".py": TextLoader,
    # ".pdf": PDFMinerLoader,
    ".pdf": PyMuPDFLoader,
    ".csv": CSVLoader,
    ".xls": UnstructuredExcelLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".docx": Docx2txtLoader,
    ".doc": Docx2txtLoader,
}

query = """
    abstracts of this paper, conclusion of this paper, hypothesis development, trading strategies, data and methodologies, sharpe, annual returns, profit, outperform the market, hypothesis, sample period, risk management
"""

input_tem = """
You are an expert researcher exceling in summarize research paper to find trading strategies. I want you to help me summarizing paper. Please read carefully the following document extracted from a paper:

<document>
{document}
</document>

First, please check if you know which paper this document is extracted from?
Now, from only: 
[1] the information given in the documents
[2] the knowledge if you have of the paper that this document extracted from 
[3] your ability to deduce from information
, please generate summarization of paper in form of Json with the attributes explained as the following:

<instruct>
{instruct}
</instruct>

For example: 

<example>
{example}
</example>

Output must only be a string with json format like the example, nothing else.
"""

exam_tem = '''
When reading a paper name: Disagreement in Option Market and Cross Section Stock Returns, we expect your output like this:
{
"Title": "Disagreement in Option Market and Cross Section Stock Returns"
"Authors": "ZHU Cai"
"Issued year": "2019"
"Research subject / Main focus": "The paper investigates the relationship between option trading volume and open interest distributions across various strike levels and their impact on expected stock returns."
"Key words": "Option strike dispersion, belief dispersion, option trading volume, open interest, stock returns, Miller (1977) theory"
"Hypothesis": "The hypothesis is that higher option strike dispersion correlates with lower future stock returns, consistent with Miller's (1977) theory on investor belief dispersion."
"Key finding": "The paper finds a significant negative relationship between option strike dispersion and future stock returns, supporting the hypothesis that higher dispersion reflects greater disagreement among investors, leading to lower returns."
"Implication":  "The strategy performs particularly well during times of market stress, with higher returns observed during crises when high dispersion stocks are heavily discounted. \nThe dispersion measure used outperforms traditional analyst forecast dispersion measures in predicting stock returns. \nThe study shows that the relationship between option strike dispersion and returns is robust over time and consistent across different market conditions."
"Trading strategy": "Long stocks with low option strike dispersion and short those with high option strike dispersion."
"Sample period": "01/1996 to 12/2012"
"Sample market": "US Stock market"
"Sample size": "Top 1000 capitalization stock (or Russell 3000, or S&P500 stocks)"
"Backest results": "The long-short strategy earns an annualized abnormal return of 14.05% with a Sharpe ratio of 0.79."
"Risk management": "The paper suggests managing risk by scaling exposure based on trailing volatility, reducing negative skewness and enhancing returns."
}
'''
main_signal = "The main indicator used as the signal in a trading strategy paper is typically the key metric or variable that triggers buy or sell decisions, such as the spread between implied volatilities, moving averages, or specific ratios like the put-call ratio. This indicator forms the basis for generating trading signals"

instruct_tem = '''
Please noted thata attributes like: [Title, Authors, Issued date, Research subject / Main focus, Key words] usually located at the very first of document. 

Title: the name of this paper, summarizes the focus of the paper and its main research question or topic
Authors: researchers who conducted the study
Issued year: when the paper was published
Research subject / Main focus: describes the primary topic or question the paper addresses and the core aspect of the research.
Key words: highlight important concepts or methods used.
Hypothesis: the initial assumption or prediction the paper tests, based on theoretical or empirical expectations.
Key finding: the main results or conclusions of the paper, explaining how the data or analysis supports the hypothesis.
Implication: describe the practical or theoretical significance of the findings, including how they might affect practices, policies, or further research.
Trading strategy: best trading strategy suggested by the paper or infer by you, must specificaly formatted: long (buy) and short (sell) which stocks based on certain criteria.
Sample period: the timeframe during which the data was collected or analyzed.
Sample market: the market or geographic area covered in the study.
Sample size: the number of observations or units analyzed in the study.
Backest results: (prioritize Return and Sharpe ratio if provided) all the performance metrics of the paper for any strategy or methodology tested, such as returns, sharpes, significant at the which level, standard deviation, and more. 
Risk management: includes strategies or recommendations for managing potential risks associated with the findings or strategies proposed.
'''

input_tem_super = """
You are an expert researcher exceling in summarize to find trading strategies. I want you to help me summarizing this. Please read carefully the following document extracted from a paper:

<document>
{document}
</document>

First, please check if you know which paper this document is extracted from?
Now, from only: 
[1] the information given in the documents
[2] the knowledge if you have of the paper that this document extracted from 
[3] your ability to deduce from information
,please generate summarization of paper in form of Json with the attributes explained as the following:

<instruct>
{instruct}
</instruct>

For example: 

<example>
{example}
</example>

Output must only in the json format like the example, nothing else.
"""

exam_tem_super = '''
When reading this:
{
"Title": "Disagreement in Option Market and Cross Section Stock Returns"
"Authors": "ZHU Cai"
"Issued year": "2019"
"Research subject / Main focus": "The paper investigates the relationship between option trading volume and open interest distributions across various strike levels and their impact on expected stock returns."
"Key words": "Option strike dispersion, belief dispersion, option trading volume, open interest, stock returns, Miller (1977) theory"
"Hypothesis": "The hypothesis is that higher option strike dispersion correlates with lower future stock returns, consistent with Miller's (1977) theory on investor belief dispersion."
"Key finding": "The paper finds a significant negative relationship between option strike dispersion and future stock returns, supporting the hypothesis that higher dispersion reflects greater disagreement among investors, leading to lower returns."
"Implication":  "The strategy performs particularly well during times of market stress, with higher returns observed during crises when high dispersion stocks are heavily discounted. \nThe dispersion measure used outperforms traditional analyst forecast dispersion measures in predicting stock returns. \nThe study shows that the relationship between option strike dispersion and returns is robust over time and consistent across different market conditions."
"Trading strategy": "Long-short strategy that involves purchasing stocks with low option strike dispersion and shorting those with high option strike dispersion. The strategy is tested across various periods and market conditions."
"Sample period": "01/1996 to 12/2012"
"Sample market": "US Stock market"
"Sample size": "Top 1000 capitalization stock (or Russell 3000, or S&P500 stocks)"
"Backest results": "The long-short strategy earns an annualized abnormal return of 14.05% with a Sharpe ratio of 0.79."
"Risk management": "The paper suggests managing risk by scaling exposure based on trailing volatility, reducing negative skewness and enhancing returns."
}

We expect your output:
{
"Title": "Disagreement in Option Market and Cross Section Stock Returns",
"Authors": "ZHU Cai",
"Issued year": "2019",
"Hypothesis": "The hypothesis is that higher option strike dispersion correlates with lower future stock returns, consistent with Miller's (1977) theory on investor belief dispersion.",
"Trading strategy": "Long stocks with low option strike dispersion and short those with high option strike dispersion. The strategy is tested across various periods and market conditions.",
"Testing period": "01/1996 to 12/2012",
"Finding": "The paper finds a significant negative relationship between option strike dispersion and future stock returns, supporting the hypothesis that higher dispersion reflects greater disagreement among investors, leading to lower returns.",
"Quantitative Results": "Sharpe ratios: 0.79; Return: 14.05%; Significant at the level of 1%"
}
'''

instruct_tem_super = '''
"Title": name of the paper, reflecting main topic or focus of the paper
"Authors": Who conducted the study
"Issued year": When the paper was published
"Hypothesis": initial prediction or assumption being tested
"Trading strategy": with the format of: Long stocks with a trait and short stock with a trait
"Testing period": timeframe during which the test was conducted 
"Finding": main result or conclusion of the study
"Quantitative Results": Based on the results from the backtest results inputed, extract the key metrics 
'''














os.environ["OPENAI_API_KEY"] = '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'