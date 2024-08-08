#import all libraries
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="PenPaper Analytics",
                   page_icon="📊")

#title 
st.title(":green[PenPaper] Analytics...")
st.subheader("GET YOUR :grey[(csv,xlxs)] DATA EXPLORED",divider="gray")
file = st.file_uploader("Drop your CSV or XLSX file", type=["csv","xlsx"])
if (file !=None):
    if (file.name.endswith("csv")):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    st.dataframe(data)
    st.success("File is Sucessfuly uploaded", icon="✅")

    st.subheader(":blue[Here's the Basic Info of data]",divider="gray")

    #tabs
    tab1,tab2,tab3,tab4 = st.tabs(["Summary", "Top & Bottom Rows", "Data Type", "Column Names"])

    with tab1:
        st.write(f"There are :blue[{data.shape[0]} rows] and :blue[{data.shape[1]} columns] in the data set.")
        st.subheader(":grey[Statistical Summary]")
        st.dataframe(data.describe())

    with tab2:
        st.subheader(":grey[Top Rows]")
        toprows = st.slider("Number of rows you want: ", 0,data.shape[0],key="topslider")
        st.dataframe(data.head(toprows))

        st.subheader(":grey[Bottom Rows]")
        bottomrows = st.slider("Number of rows you want: ", 0,data.shape[0],key="bottomslider")
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(":grey[Data type of cols]")
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader(":grey[Columns name in dataset]")
        st.write(list(data.columns))
 

    st.subheader(":blue[Column Values to Count]", divider="gray")
    #expander used open when clicked
    with st.expander("Value Count"):
        col1,col2=st.columns(2)
        with col1:
            column = st.selectbox("Choose Column Name", options=list(data.columns))
        with col2:
            toprows = st.number_input("Choose Top Rows", min_value=1,step=1)

        count = st.button("Count")
        if count==True:
            result=data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)

            # visualization
            st.subheader("Visualization", divider="grey")

            #bar chart
            fig = px.bar(data_frame=result, x=column, y="count",text="count",template='plotly_white') 
            st.plotly_chart(fig)

            #linechart
            fig = px.line(data_frame=result,x=column,y="count",text="count",template="plotly_white")
            st.plotly_chart(fig)

            #piechart
            fig=px.pie(data_frame=result,names=column,values="count")
            st.plotly_chart(fig)
            

    #group by 
    st.subheader(":blue[GroupBy:] Simplify Your Data Analysis]")
    st.write(" Allows you to Summarize data based on specific category and groups.")
    with st.expander("GroupBy your Columns"):
        col1,col2,col3 = st.columns(3)
        with col1:
            #multiselesct to aloow to select multiple cols:
            groupby_cols = st.multiselect("Choose column to GroupBy",options=list(data.columns))

        with col2:
            operation_cols = st.selectbox("Select Operation",options=list(data.columns))

        with col3:
            operation = st.selectbox("Choose Operation to Perform",options=["sum","min","count","max","mean","median"])   


        if groupby_cols:
            result=data.groupby(groupby_cols).agg(
                newcol=(operation_cols,operation)
            ).reset_index()
            st.dataframe(result)
             
             #visualization
            st.subheader("Data Visualization")
            graphs =st.selectbox("Choose your Graph",options=["line","bar","scatter","pie","sunburst"])
            if (graphs=="line"):
                x_axis =st.selectbox("Choose the X-axis",options=list(result.columns))
                y_axis =st.selectbox("Choose the Y-axis",options=list(result.columns))
                #none will be by default
                colour = st.selectbox("Colour Information",options=[None] +list(result.columns))
                fig=px.line(data_frame=result,x=x_axis,y=y_axis,color=colour,markers="o")
                st.plotly_chart(fig)

            elif(graphs=="bar"):
                x_axis =st.selectbox("Choose the X-axis",options=list(result.columns))
                y_axis =st.selectbox("Choose the Y-axis",options=list(result.columns))
                colour = st.selectbox("Colour Information",options=[None] +list(result.columns))
                facet_col = st.selectbox("Column Information",options=[None] +list(result.columns))
                fig=px.bar(data_frame=result,x=x_axis,y=y_axis,color=colour,facet_col=facet_col,barmode="group")
                st.plotly_chart(fig)

            elif(graphs=="scatter"):
                x_axis =st.selectbox("Choose the X-axis",options=list(result.columns))
                y_axis =st.selectbox("Choose the Y-axis",options=list(result.columns))
                colour = st.selectbox("Colour Information",options=[None] +list(result.columns))
                size = st.selectbox("Size Column",options=[None] +list(result.columns))
                fig = px.scatter(data_frame=result,x=x_axis,y=y_axis,color=colour,size=size)
                st.plotly_chart(fig)

            elif(graphs=="pie"):
                values=st.selectbox("Choose Numerical Values",options=list(result.columns))
                names=st.selectbox("Choose Labels",options=list(result.columns))
                fig = px.pie(data_frame=result,values=values,names=names)
                st.plotly_chart(fig)

            elif(graphs=="sunburst"):
                path = st.multiselect("Choose your path",options=list(result.columns))
                fig = px.sunburst(data_frame=result,path=path,values="newcol")
                st.plotly_chart(fig)
                



