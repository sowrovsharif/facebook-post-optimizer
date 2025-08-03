import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

def get_time_period(hour):
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"

def train_model(df):
    df['TimePeriod'] = df['Post Hour'].apply(get_time_period)
    X = df[['Type', 'Post Weekday', 'Post Hour', 'Paid', 'Page total likes', 'Category']]
    y = df['Lifetime Post Total Reach']

    categorical = ['Type', 'Paid', 'Category']

    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical)
    ], remainder='passthrough')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = make_pipeline(preprocessor, RandomForestRegressor(random_state=42))
    model.fit(X_train, y_train)
    return model

def interpret_prediction(model, post_type, weekday, hour, paid, page_likes, category):
    sample = pd.DataFrame([{
        'Type': post_type,
        'Post Weekday': weekday,
        'Post Hour': hour,
        'Paid': paid,
        'Page total likes': page_likes,
        'Category': category
    }])

    prediction = model.predict(sample)[0]

    weekday_map = {
        1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday',
        5: 'Thursday', 6: 'Friday', 7: 'Saturday'
    }
    time_period = get_time_period(hour)

    return f"📢 Prediction: On {weekday_map[weekday]} at {hour}:00 ({time_period}), posting a {post_type} under '{category}' category (with ~{page_likes:,} page likes) may reach approximately {int(prediction):,} people."
