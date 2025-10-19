#!/bin/bash
if [ -z "$PORT" ]; then
    export PORT=8501
fi
echo "Starting Streamlit on port $PORT"
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0