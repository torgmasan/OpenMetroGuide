# OpenMetroGuide

![Admin](Pictures/admin.png?raw=true "ADMIN")
![Admin Zoom](Pictures/admin_zoom.png?raw=true "ADMIN")
![Client](Pictures/client.png?raw=true "ADMIN")

Python application which enables users to create metro maps (Admins) and
find a path from a starting station to a final destination, with the constraints of
either distance or time.



### Requirements
```
python (3.9+)

pygame

sqlite3
```

### Features

* Create and Edit Metro Maps
  * Use 8 colors to represent different lines
  * Auto-save when closing window
* Store Metro Maps
  * Any number of maps can be stored for later editing/viewing
* Find shortest/cheapest path from one station to another by constraining Cost/Distance
* Zoom in/out while editing/viewing (<kbd>Ctrl</kbd> + <kbd>P</kbd>/<kbd>Ctrl</kbd> + <kbd>M</kbd>)
* Shift right/left while editing/viewing (<kbd><</kbd> / <kbd>></kbd>)
    
### Notes

OpenMetroGuide saves metro maps on the local desktop itself. The project
can be made more potent as a web application.
