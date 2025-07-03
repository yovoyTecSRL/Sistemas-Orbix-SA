#!/bin/bash
cd /workspaces/Sistemas-Orbix-SA/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
