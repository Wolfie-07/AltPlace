# handlers/__init__.py

from handlers.start import router as start_router
from handlers.cafes import router as cafes_router
from handlers.help import router as help_router
from handlers.filter import router as filter_router
from handlers.suggest import router as suggest_router  # ✅ Add this
from handlers.profile import router as profile_router  # ✅ Add this
from handlers.meetup import router as meetup_router  # ✅ Add this
from handlers.contact import router as contact_router  # ✅ Add this
from handlers.createmeetup import router as createmeetup_router  # ✅ Add this
from handlers.library import router as library_router  # ✅ Add this
from handlers.venues import router as venues_router  # ✅ Add this  
from handlers.my_meetups import router as my_meetups_router  # ✅ Add this
# Collect all routers in a list
routers = [
    start_router,
    cafes_router,
    filter_router,
    help_router,
    suggest_router,
    profile_router,
    meetup_router,
    contact_router,
    createmeetup_router,
    library_router,
    venues_router,
    my_meetups_router# ✅ Register here
]





