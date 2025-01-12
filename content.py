# feature importances
from rfpimp import permutation_importances
from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

# clustering 1d array
from scipy.signal import argrelextrema
from sklearn.neighbors.kde import KernelDensity

# data processing
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd

# text processing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


import warnings
warnings.filterwarnings('ignore')

class content :
    def content_based(my_course):

        data = pd.read_csv("Coursera.csv", encoding='latin-1')
        df = data.dropna(subset=['keyword'])

        df = df.replace('', np.nan)

        cols = [
            'name',
            'title_type',
            'rating',
            'num_votes',
            'start_year',
            'course_url',
            'course_id',
            'keyword',
        ]

        le = LabelEncoder()
        dataset = df[cols].dropna().copy()
        dataset['title_type'] = le.fit_transform(dataset['title_type'])

        def imp_df(column_names, importances):
            data = {
                'Feature': column_names,
                'Importance': importances,
            }
            df = pd.DataFrame(data) \
                .set_index('Feature') \
                .sort_values('Importance', ascending=False)
            
            return df

        def r2(rf, X_train, y_train):
            return r2_score(y_train, rf.predict(X_train))

        def drop_col_feat_imp(model, X_train, y_train, random_state=42):
            model_clone = clone(model)
            model_clone.random_state = random_state
            
            model_clone.fit(X_train, y_train)
            benchmark_score = model_clone.score(X_train, y_train)
            
            importances = []
            
            for col in X_train.columns:
                model_clone = clone(model)
                model_clone.random_state = random_state
                model_clone.fit(X_train.drop(col, axis=1), y_train)
                drop_col_score = model_clone.score(X_train.drop(col, axis=1), y_train)
                importances.append(benchmark_score - drop_col_score)
            
            return imp_df(X_train.columns, importances)

        X = dataset.drop(['rating', 'name', 'keyword', 'course_id', 'course_url'], axis=1)
        y = dataset['rating']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=0)

        rf = RandomForestRegressor(n_estimators=100 , max_features='auto', oob_score=True , n_jobs=-1 , random_state=42 , min_samples_leaf=0.05).fit(X_train, y_train)


        dataset['score'] = (
            0.40 * dataset['num_votes']  + 
            0.30 * dataset['start_year'] + 0.30 * dataset['title_type']
        )

        dataset = dataset.reset_index(drop=True)

        vals = dataset['score'].values.reshape(-1, 1)
        kde = KernelDensity(kernel='gaussian', bandwidth=3).fit(vals)

        s = np.linspace(650, 20000)
        e = kde.score_samples(s.reshape(-1,1))

        mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]

        points = np.concatenate((s[mi], s[ma]), axis=0)
        buckets = []

        for point in points:
            buckets.append(point)

        buckets = np.array(buckets)
        buckets.sort()

        dataset['cluster'] = buckets.searchsorted(dataset.score)

        tfidf_vectorizer = TfidfVectorizer()
        matrix = tfidf_vectorizer.fit_transform(dataset['keyword'])

        def get_recommendations(movie_index):
            print(dataset['name'].iloc[movie_index])
            
            kernel = linear_kernel(matrix[movie_index], matrix)
            sim_scores = list(enumerate(kernel[0]))
            
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            indexes = [i[0] for i in sim_scores if i[0] != movie_index and i[1] > .5]
            
            cond1 = (dataset.index.isin(indexes))
            cond2 = (dataset.cluster == dataset.iloc[movie_index]['cluster'])
            cond3 = (dataset.title_type == dataset.iloc[movie_index]['title_type'])
            
            selected = dataset.loc[cond1 & cond2 & cond3] \
                .sort_values(by='rating', ascending=False).head(20)
            # print(selected)
            my_list = []
            for name in selected['name'] :
                my_list.append(name)
            return my_list
        
        x = None
        df = data[['name','index']].values.tolist()
        for name,index in df:
            if(name == my_course):
                x = index
                break
        # print(x)

        my_list = get_recommendations(x)
        return my_list
        # print()
        # for i in my_list :
        #     print(i)
        
