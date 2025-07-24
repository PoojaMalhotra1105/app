import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Maven Bookshelf", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(/Users/poojam/Downloads/maven_bookshelf_app/goodreads_works.csv
poojam@Poojas-MacBook-Air maven_bookshelf_app %)
    return df

df = load_data()

# Clean missing titles
df = df[df["title"].notna()]

# Sidebar Filters
st.sidebar.header("🔍 Filter Books")
min_rating = st.sidebar.slider("Minimum average rating", 0.0, 5.0, 3.5, 0.1)
min_reviews = st.sidebar.slider("Minimum number of ratings", 0, 1000000, 1000, step=1000)
title_search = st.sidebar.text_input("Search by book title")

# Filter data
filtered_df = df[
    (df["average_rating"] >= min_rating) &
    (df["ratings_count"] >= min_reviews)
]

if title_search:
    filtered_df = filtered_df[filtered_df["title"].str.contains(title_search, case=False)]

# Title
st.title("📚 Maven Bookshelf Explorer")

st.markdown("Explore Goodreads books data from the Maven Challenge. Use the sidebar to filter books by rating, reviews, or search by title.")

# Show top results
st.subheader("📘 Top Books")
st.write(f"Showing {filtered_df.shape[0]} books matching your criteria.")
st.dataframe(
    filtered_df[["title", "authors", "average_rating", "ratings_count"]]
    .sort_values(by="average_rating", ascending=False)
    .head(20),
    use_container_width=True
)

# Top Authors
st.subheader("👩‍💻 Top Authors by Average Rating")
top_authors = (
    filtered_df.groupby("authors")["average_rating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

chart = alt.Chart(top_authors).mark_bar().encode(
    x=alt.X("average_rating:Q", title="Average Rating"),
    y=alt.Y("authors:N", sort="-x", title="Author"),
    tooltip=["authors", "average_rating"]
).properties(height=400)

st.altair_chart(chart, use_container_width=True)

# Ratings distribution
st.subheader("📈 Ratings Distribution")
hist = alt.Chart(filtered_df).mark_bar().encode(
    alt.X("average_rating:Q", bin=alt.Bin(maxbins=30), title="Average Rating"),
    alt.Y("count()", title="Number of Books"),
    tooltip=["count()"]
).properties(height=300)

st.altair_chart(hist, use_container_width=True)

