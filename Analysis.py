import pandas as pd
import plotly.express as px
import streamlit as st
import statsmodels.api as sm
import plotly.graph_objects as go

# st.set_page_config(page_title="Main Analysis")

cedf = pd.read_csv("CO2 Emissions_Canada.csv")


average_per_make = cedf.groupby("Make", as_index=False).mean()
sorted_brands_per_emission = average_per_make.sort_values("CO2 Emissions(g/km)").reset_index()
tmb = sorted_brands_per_emission.iloc[[0,1,20,21, 40, 41]].reset_index()
tmb['Price'] = ['Low', 'Low', 'Middle', 'Middle', 'High', 'High']
Pastel1 = px.colors.qualitative.Pastel1
Burgyl = px.colors.sequential.Burgyl

st.title("CO2 emissions of cars in North America")


st.header("Overview")
st.write("In this analysis the following question was explored: What factors influence CO2 emissions  of cars?")
st.write("The data set looked at: brand, model, vehicle size, engine size(L), number of cylinders, type of transmission, fuel type, fuel consumption, and CO2 emissions(g/km).")
st.write(" After cleaning the data it was decided to focus on: Make of car, CO2 emissions (g/km), Engine Size(L), Cylinders, and Price.")
st.write("It is hypothesized that the most expensive makes, cars with larger engines, and cars that have more cylinders will produce the most CO2 emissions.")

st.header("Car Make Relations with Average CO2 Emissions, Average Amount of Cylinders, and Average Engine size (L)")
fig = px.bar(sorted_brands_per_emission, x='Make', y='CO2 Emissions(g/km)', title="The Relationship Between the Make of Car and average CO2 Emissions", color_discrete_sequence=Pastel1)
st.plotly_chart(fig)
st.write("In the graph above it can be shown that there are 42 makes of cars. The makes are ascending by the average amount of CO2 emissions across the data for that make. The furthest left make of car, Smart,  has the least CO2 emissions on average  while the furthest right make of car, Bugatti, produces the most CO2 emissions on average. The amount of CO2 emissions is also shown by how tall the bars are which corresponds to the numbers on the side of the bar graph.")

fig = px.bar(sorted_brands_per_emission, x='Make', y='Cylinders',color_discrete_sequence=Pastel1, title="The Relationship Between the Make of car and average amount of Cylinders") 
st.plotly_chart(fig)
st.write("In the graph above it can be shown that there are 42 makes of cars. The makes are ascending by the average amount of CO2 emissions across the data for that make. The furthest left make of car, Smart, has the least CO2 emissions on average while the furthest right make of car, Bugatti, produces the most CO2 emissions on average. The amount of cylinders is also shown by how tall the bars are which corresponds to the numbers on the side of the bar graph. There is a general positive trend that can be seen going across the graph. This represents that in general, the more average CO2 emissions produced by the make of car increases when average number of cylinders also increase.")

fig = px.bar(sorted_brands_per_emission, x='Make', y='Engine Size(L)', color_discrete_sequence=Pastel1, title="The Relationship Between the Make of Car and average Engine Size (L)") 
st.plotly_chart(fig)
st.write("In the graph above it can be shown that there are 42 makes of cars. The makes are ascending by the average amount of CO2 emissions across the data for that make. The furthest left make of car, Smart,  has the least CO2 emissions on average  while the furthest right make of car , Bugatti, produces the most CO2 emissions on average. The average engine size of those makes is also shown by how tall the bars are which corresponds to the numbers on the side of the bar graph. There is a general positive trend that can be seen going across the graph. This represents that in general, the more average CO2 emissions produced by the make of car increases when average engine size also increases.")


#Nasinya
st.header("CO2 Averages and Distributions")
fig = px.box(cedf[cedf['Make'].isin(['SMART', 'HONDA','AUDI','BMW','LAMBORGHINI','BUGATTI'])].sort_values('CO2 Emissions(g/km)'), x='Make', y= "CO2 Emissions(g/km)",color_discrete_sequence=Pastel1, title='Representation of CO2 Emissions by Make')
st.plotly_chart(fig)
st.write ("This graph uses six makes from the list of 42 that are from different parts of the list when ranked by emissions. A box graph is used to show the distribution of the data for each of the different makes. The filled in boxes show where most of the information lies, and the colored horizontal lines represent where most of the information ends. Dots are used to show anomalies that do not match the majority of the data. The first two (moving left to right) have the lowest emissions per kilometer. It is shown by the box graph that the Honda sample’s emissions per kilometer span from around 100-275 g/km whereas the Smart Car’s emission rates are stable at around 150 g/km. This suggests that Smart Car has many similar models, and focuses on efficient emissions. Both Audi and BMW emit a medium amount of carbon per kilometer which is represented on the graph. Lamborghini and Bugatti emit very large amounts of carbon on average. There is a good amount of information about different Lamborghini models, so the different emission rates are easy to observe, but there is only data about one Bugatti model so there is not an accurate representation of all Bugatti cars. Overall, this graph allows us to easily compare the distributions of emissions for each of the models of six different makes.")

st.header("CO2 Averages and Price")
fig = px.bar(tmb, x='Make', y='CO2 Emissions(g/km)', color='Price', color_discrete_sequence=Pastel1, title='CO2 Emissions(g/km) by Make vs. Price')
st.plotly_chart(fig)
st.write ("The above graph shows six makes of cars in order of their average CO2 emissions per kilometer, and the colors of the columns represent the price range. The first two makes (going left to right), Smart and Honda, emit the least carbon per kilometer out of the 42 makes in the data set, and are also the lowest in price of these six. The second two makes, Audi and BMW, emit a medium amount of CO2 per kilometer as they are found in the exact middle of the emissions ranking, they are also in the medium price range. Lamborghini and Bugatti emit the most of the 42 makes on average, and are also very high in price. This data proves our hypothesis, which was that the average carbon emissions of gasoline cars per kilometer increase with the price of the car."
)

#Lowest Amount of Cylinders vs CO2 Emission (Sameer)
bottom_cylinders = average_per_make.sort_values("Cylinders").head(20).reset_index()
bottom_cylinders.dropna()

cylinder_low_emission = px.scatter(bottom_cylinders, x="Cylinders", y="CO2 Emissions(g/km)", title='Cylinders Amount and CO2 Emission Graph', size='Cylinders', hover_data=['Make'], color='Make', color_continuous_scale=Burgyl)

model = sm.OLS(bottom_cylinders["CO2 Emissions(g/km)"], bottom_cylinders['Cylinders']).fit()
fitted = model.fittedvalues
cylinder_low_emission.add_trace(go.Scatter(x=bottom_cylinders['Cylinders'],
                         y=fitted,
                         mode='lines',
                         name='best fit',
                         line=dict(color='#acafba', width=2)
                        ))
# cylinder_low_emission.show()


#Most Cylinders vs CO2 Emission (Sameer)
st.header("The Relationship Between the Cylinders and the CO2 emissions")
top_cylinders = average_per_make.sort_values("Cylinders").tail(20).reset_index()
top_cylinders.dropna()

cylinder_high_emission = px.scatter(top_cylinders, x="Cylinders", y="CO2 Emissions(g/km)", title='Cylinders Amount and CO2 Emission Graph', size='Cylinders', hover_data=['Make'], color='Make',color_continuous_scale=Burgyl)

model = sm.OLS(top_cylinders["CO2 Emissions(g/km)"], top_cylinders['Cylinders']).fit()
fitted = model.fittedvalues
cylinder_high_emission.add_trace(go.Scatter(x=top_cylinders['Cylinders'],
                         y=fitted,
                         mode='lines',
                         name='best fit',
                         line=dict(color='#acafba', width=2)
                        ))
# cylinder_high_emission.show()
st.plotly_chart(cylinder_low_emission)
st.plotly_chart(cylinder_high_emission)

st.write("The x-axis is the number of cylinders in a car, and the y-axis is the CO2 emissions in g/km. Each plot has a specific color that corresponds to the make of the vehicle, and the size of the plot varies depending on the number of cylinders. From the graph, it is clear that as the number of cylinders increases, so do the grams of carbon dioxide emissions per kilometer. Also, the car with the lowest amount of cylinders (the Smart car) has the lowest amount of CO2 emissions, while the Bugatti has the highest CO2 emissions with the highest amount of cylinders. The line of best fit shows that this is a positive trend. There may be some inconsistency in the CO2 emissions of cars with the same number of cylinders, but these are due to external factors. This graph answers our question and proves our hypothesis, as the number of cylinders is something that affects CO2 emissions.")


#Brand engine size vs CO2 emission (Leo)
average_engine_size = cedf.groupby("Make", as_index=False).mean("Engine Size(L)")
st.header("The Relationship Between the Engine size (L) and the CO2 emissions")
#Total emissions brands compared with engine size
fig_total = px.scatter(cedf, x='Engine Size(L)', y='CO2 Emissions(g/km)', color='Make',title="The Relationship Between Total CO2 Emissions makes and the Average Engine Size(L)",color_continuous_scale=Burgyl)
st.plotly_chart(fig_total)
st.write("From the scatter plot of all data points suggests that: The CO2 emission different among the same engine size or make of car, but the CO2 emission is generally positively related with the engine size. The ordinary least square line has a positive slope, which helps to prove the positive relationship between the engine size and CO2 emissions. It is suggested that the engine size might be a factor which influence the cars' CO2 emission. However, when looking along the x-axis, it can be shown that some cars of different engine size have the same CO2 emission. In order to investigate this more,  the average engine size of different make of car compared with the average CO2 emission is introduced.")
#Higher C02 emissions brands (high 10) compared with average engine size
fig_high = px.scatter(sorted_brands_per_emission.tail(10), x='Engine Size(L)', y='CO2 Emissions(g/km)',color='Make', trendline="ols",title="The Relationship Between Higher CO2 emissions makes of cars(highest 10) and average engine size",color_continuous_scale=Burgyl)
st.plotly_chart(fig_high)
st.write("Looking at the graph, it shows the 10 highest producing car makes, averaged across their models, of CO2 emission and the average engine sizes of their models. The average engine size of the 10 highest producing car makes is positively related to the CO2 emissions, meaning that a larger engine usually means more emissions.")
#Lower C02 emissions brands (low 10) compared with average engine size
fig_low = px.scatter(sorted_brands_per_emission.head(10), x='Engine Size(L)', y='CO2 Emissions(g/km)',color='Make', trendline="ols",title="The Relationship Between Lower CO2 emissions makes of cars(lowest 10) and average engine size",color_continuous_scale=Burgyl)
st.plotly_chart(fig_low)
st.write("Looking at the graph, it shows the 10 lowest producing car makes of CO2 emission and the engine sizes. The average engine size of the 10 lowest producing car makes is positively related to the CO2 emissions. Drawing conclusions from both graphs, it can be shown that even on both extremes a larger engine indicates a larger CO2 emission.")

st.header("Conclusion")
st.write("In conclusion, the most expensive makes of cars, cars with larger engines, and cars that have more cylinders will produce the most CO2 emissions as supported through the visualizations and analyses.")


st.write("Sources:")
st.write("We used a data set from Kaggle, which is a platform used to share and find data sets and code. If your would like more information about the data we used you can visit this link: https://www.kaggle.com/datasets/debajyotipodder/co2-emission-by-vehicles")
st.write("The information on make prices was not included in the main data set, most of the numbers were found on this website:https://www.usnews.com/")
