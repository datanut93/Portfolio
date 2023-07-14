import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
#from sklearn.tree import export_graphviz
#from sklearn.inspection import plot_partial_dependence
import pydot as pydot
#from dtreeviz.trees import dtreeviz

url = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'
data = pd.read_csv(url)


# Clean data
##data = data.drop(["Name", "Ticket", "Cabin"], axis=1)  # Remove unnecessary columns
data = data.dropna()  # Remove rows with missing values

# Convert categorical variables to numerical variables
data["Sex"] = np.where(data["Sex"] == "female", 1, 0)

    # Create a new column indicating whether the passenger survived or not
data['Survived Text'] = data['Survived'].map({0: 'No', 1: 'Yes'})



# Define input features and target variable
X = data[["Pclass", "Sex", "Age", "Fare"]]
y = data["Survived"]

# Train a random forest classifier
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
rf.fit(X, y)

# Define function to predict survival percentage
def predict_survival_percentage(pclass, sex, age, fare):
    input_data = np.array([[pclass, sex, age, fare]])
    prob = rf.predict_proba(input_data)[0][1]
    return prob


# Define a function to predict survival given user input
def predict_survival(pclass, sex, age, fare):
    input_data = np.array([[pclass, sex, age,  fare]])
    pred = rf.predict(input_data)[0]
    if pred == 0:
        return "not have survived"
    else:
        return "have survived"

# Define the Streamlit app
def app():
    # Define app title
    st.title("Titanic Survival Prediction")
    st.text('Use this tool to input passenger data and receive a prediction of')
    st.text('whether they would have survived based off of those variables.')
    

    
    # Define input widgets
    pclass = st.selectbox("TicketClass", [1, 2, 3])
    sex = st.selectbox("Sex", ["Male", "Female"])
    age = st.slider("Age", min_value=0, max_value=100, value=30)
   ## sibsp = st.slider("Number of Siblings/Spouses Aboard", min_value=0, max_value=8, value=0)
   ## parch = st.slider("Number of Parents/Children Aboard", min_value=0, max_value=6, value=0)
    fare = st.slider("Fare", min_value=0, max_value=600, value=30)

    # Predict survival
    if st.button("Predict"):
        sex = 1 if sex == "Female" else 0  # Convert sex to numerical variable
        result = predict_survival(pclass, sex, age, fare)
        #st.success(f"The passenger likely would  {result}.")
        survival_rate = rf.predict_proba(np.array([[1, sex, age, fare]]))[0][1]        
        st.success(f"The passenger likely would have survived with a {round(survival_rate*100, 2)}% chance.")
        
 # Create scatter plot
##fig = px.scatter(data, x="Age", y="Fare", color="Survived", labels={"Survived": "Survived?"})
##st.plotly_chart(fig)


   # ages = range(0, 80, 1)
   # survivals = [rf.predict_proba(np.array([[1, 1, age, 30]]))[0][1] for age in ages]  # Assuming female and fare=30
   # df = pd.DataFrame({"Age": ages, "Survival Rate": survivals})
   # fig = px.scatter(df, x="Age", y="Survival Rate", labels={"Age": "Age", "Survival Rate": "Survival Rate"})
   # fig.update_layout(title='Predicted Survival Coefficient by Age')
   # st.plotly_chart(fig)
    
    st.subheader("Feature Importance Plot")
    feature_importances = pd.DataFrame(rf.feature_importances_, index=X.columns, columns=["Importance"])
    feature_importances = feature_importances.sort_values(by="Importance", ascending=False)
    st.write(feature_importances)
    fig, ax = plt.subplots(1,1)
    sns.barplot(x="Importance", y=feature_importances.index, data=feature_importances, ax=ax)
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")
    st.pyplot(fig)

 # Plot decision tree
    # Display decision tree using dtreeviz
    #st.subheader("Decision Tree Visualization")
    #tree = rf.estimators_[0]
    #viz = dtreeviz(tree, X, y,
     #              feature_names=X.columns,
     #              class_names=["not survived", "survived"],
      #             fancy=True)
    #st.write(viz)    
    
   
if __name__ == "__main__":
    app()
