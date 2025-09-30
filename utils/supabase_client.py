import os
import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = os.environ["SUPABASE_URL"] = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"] = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
