# librairies
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt


class CryptoStrategy:
    def __init__(self, crypto, start_date, window):
        self.crypto = crypto
        self.start_date = start_date
        self.window = window
        self.df = None
        self.lsma_arr = []
        self.date_arr = []
        self.lsma_df = None
        self.all_df = None
        self.buydates = []
        self.selldates = []
        self.buyprices = []
        self.sellprices = []
        self.benefices = None
    
    def get_data(self):
        print("Analysing ", self.crypto, "asset")
        # importer les données
        self.df = yf.download(self.crypto, start=self.start_date)
    
    def calculate_lsma(self):
        for i in range(len(self.df) - (self.window - 1)):
            
            # aller au second lignes de l'iteration
            input_reg = self.df[i:(self.window - 1) + i]
            
            # regression OLS
            X = pd.Series(range(len(input_reg.index))).values
            y = input_reg.Close
            model = sm.OLS(y, sm.add_constant(X)).fit()
            
            # get last value
            pred = model.predict()[-1]
            
            # append
            self.lsma_arr.append(pred)
            self.date_arr.append(input_reg.iloc[-1].name)
        
        self.lsma_df = pd.DataFrame({"LSMA": self.lsma_arr}, index=self.date_arr)
        self.all_df = pd.concat([self.lsma_df, self.df], axis=1)
        self.all_df.dropna(inplace=True)
    
    def generate_signals(self):
        self.all_df['signal_achat'] = self.all_df.Close < self.all_df.LSMA
        self.all_df['signal_vente'] = self.all_df.Close > self.all_df.LSMA
        self.all_df['shifted_open'] = self.all_df.Open.shift(-1)
        
        # iterer sur le df
        in_position = False
        
        for index, row in self.all_df.iterrows():
            # si on est pas en position & signal d'achat positif
            ## acheter
            if not in_position and row.signal_achat ==True:
                buyprice = row.shifted_open # next open
                self.buyprices.append(buyprice)
                self.buydates.append(index)
                in_position = True
                
            # si on est en position & signal de vente positif
            ## vendre
            if in_position and row.signal_vente ==True:
                sellprice = row.shifted_open # next open
                self.sellprices.append(sellprice)
                self.selldates.append(index)
                in_position = False
    def generate_plot(self):
        plt.figure(figsize=(20, 8))
        plt.plot(self.all_df[['Open', 'LSMA']])
        plt.scatter(self.buydates, self.all_df.loc[self.buydates].shifted_open, marker='^', color='green')
        plt.scatter(self.selldates, self.all_df.loc[self.selldates].shifted_open, marker='v', color='red')
        plt.savefig(f'res/{self.crypto}.png')
        plt.show()
    
    def calculate_benefices(self):
        self.benefices = pd.Series([(sell - buy)/buy for sell,buy in zip(self.sellprices, self.buyprices)])
        return (self.benefices + 1).prod()
        #print("Bénéfice total :", (self.benefices + 1).prod())
        #print("Nombre de gain/perte : ", (self.benefices > 0).value_counts(normalize=True))
        #print("--"*20)


# Comment utiliser la class

# Initialize
strategy = CryptoStrategy('AAPL', '2020-01-01', 25)

# Get data
strategy.get_data()

# Calculate LSMA
strategy.calculate_lsma()

# Generate signals
strategy.generate_signals()

# generate plots
strategy.generate_plot()

# Calculate benefices
strategy.calculate_benefices()


# Tester sur plusieurs tickers
liste_symbo = pd.read_csv("https://raw.githubusercontent.com/shilewenuw/get_all_tickers/master/get_all_tickers/tickers.csv", header=None)
liste_symbo = liste_symbo[0].tolist()
liste_symbo2 = ['HLF', 'GTN', 'LAD', 'AMZN', 'FIS', 'MU', 'EDU', \
               'FISV']


# stocker les res en df             
liste_res = []
for crypto in liste_symbo[:500]:
    try:
        strategy = CryptoStrategy(crypto, '2020-01-01', 25)
        
        # Get data
        strategy.get_data() 
        
        # Calculate LSMA
        strategy.calculate_lsma()
        
        # Generate signals
        strategy.generate_signals()
        
        # generate plots
        strategy.generate_plot()
        
        # Calculate benefices
        beneficeTotal = strategy.calculate_benefices()
        liste_res.append([crypto, beneficeTotal])
    except:
        continue

# créer un dataframe pour stocker les résultats
df_res = pd.DataFrame(liste_res, columns = ['Crypto', 'BeneficeTotal'])


# visualiser les résultats
n = 20  # afficher les top n
plt.figure(figsize=(16,8))
ax = sns.barplot(x='Crypto', \
            y='BeneficeTotal', \
            data=df_res.iloc[:n,:], \
            order=df_res.iloc[:n,:].sort_values(by='BeneficeTotal', \
            ascending=False)['Crypto'])
ax.axhline(y=1, color='k', linestyle='--')
ax.axhline(y=1.5, color='g', linestyle='--')
ax.axhline(y=2, color='b', linestyle='--')
ax.axhline(y=0.5, color='r', linestyle='--')
plt.xticks(rotation=90)
plt.savefig('res:all_crypto.png')
plt.show()