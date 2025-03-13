import os
import hashlib

from fastapi import APIRouter
from datetime import datetime

from src.database.posts import *
from src.schemas.users import LoginRequest, RegisterRequest

router = APIRouter()