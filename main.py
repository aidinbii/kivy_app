from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.garden.mapview import MapView, MapMarker, MapMarkerPopup
#from kivy_garden.mapview import MapView, MapMarker, MapMarkerPopup

from kivy.graphics import Color, Rectangle, Line
import googlemaps



class Place:
    def __init__(self, name, lat, lon, description):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.description = description

class MapWithMarkers(BoxLayout):
    def __init__(self, **kwargs):
        super(MapWithMarkers, self).__init__(**kwargs)

        # Initialize Google Maps API client
        self.gmaps = googlemaps.Client(key='AIzaSyAbb4S49LTN5wRk7MfaYDXNTF-GSGshAMI')  # Replace 'YOUR_API_KEY' with your actual API key

        # Retrieve the coordinates for a location
        geocode_result = self.gmaps.geocode('Bishkek, Kyrgyzstan')
        location = geocode_result[0]['geometry']['location']
        lat, lng = location['lat'], location['lng']

        # Create a map view
        self.mapview = MapView(zoom=12, lat=lat, lon=lng)

        # Add map to the layout
        self.add_widget(self.mapview)

        # Call function to add markers
        self.add_markers_with_popups()

        # self.origin = None
        # self.destination = None
        # self.selecting_origin = False

        #  # Add a button to trigger origin/destination selection
        # self.select_button = Button(text="Select Origin", size_hint=(None, None))
        # self.select_button.bind(on_press=self.toggle_selection)
        # self.add_widget(self.select_button)
        
        # Bind the on_map_click event to the mapview
        #self.mapview.bind(on_map_click=self.on_map_click)
    

    def add_markers_with_popups(self):
        places = [
            Place(name='Compass College', lat=42.870732337549754, lon=74.58817606479953, 
                  description='Compass College is a private school in Bishkek, Kyrgyzstan.'),
            Place(name='Osh Bazaar', lat=42.87508081668895, lon=74.57023474659336, 
                  description='Osh Bazaar is a large bazaar in Bishkek, Kyrgyzstan.'),
            Place(name='Orto-Say Bazaar', lat=42.83678331061501, lon=74.61591471961715, description='Orto-Say Bazaar is another bazaar in Bishkek, Kyrgyzstan.'),
            # Add more places with their details
        ]

        for place in places:
            self.add_marker_with_popup(place)

    def add_marker_with_popup(self, place):
        marker = MapMarker(lat=place.lat, lon=place.lon, source="marker.png")
        marker.place = place  # Store the place information within the marker object
        marker.bind(on_press=self.on_marker_press)
        self.mapview.add_marker(marker)
        print(f"Added marker for {place.name} at Lat: {place.lat}, Lon: {place.lon}")
    
    def on_marker_press(self, marker):
        place = marker.place  # Retrieve the place information from the marker object
        self.show_popup(place)

    def show_popup(self, place):
        ''' 
        function creates a MapMarkerPopup with a label containing the desired text and attaches it to the map.
        '''
        popup = MapMarkerPopup(lat=place.lat, lon=place.lon, source="marker.png")
        
        box_layout = BoxLayout(orientation='vertical')
        # https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label
        label = Label(text=place.description, text_size=(box_layout.size[0], None), font_size=12, color=(1, 0, 0, 1))

        # Set background color and border for the label
        with box_layout.canvas.before:
            Color(1, 1, 1, 1)  # Set the RGBA values for the color
            Rectangle(pos=box_layout.pos, size=box_layout.size)

        box_layout.add_widget(label)
        popup.add_widget(box_layout)
        self.mapview.add_widget(popup)
        print(f"Showing popup for {place.name}")


    # def toggle_selection(self, instance):
    #     if not self.selecting_origin:
    #         self.selecting_origin = True
    #         self.select_button.text = "Select Destination"
    #     elif self.selecting_origin and not self.origin:
    #         print("Please select an origin before selecting a destination.")
    #     else:
    #         self.selecting_origin = False
    #         self.select_button.text = "Select Origin"
    #         if self.origin and self.destination:
    #             self.draw_route(self.origin, self.destination)

    # def toggle_selection(self, instance):
    #     if not self.selecting_origin:
    #         self.selecting_origin = True
    #         self.select_button.text = "Select Destination"
    #     elif self.selecting_origin and not self.origin:
    #         #self.origin = self.mapview.get_latlon_at(*self.mapview.to_window(*self.mapview.center))
    #         print(f"Origin set at: {self.origin}")
    #         self.select_button.text = "Select Origin"
    #     else:
    #         #self.destination = self.mapview.get_latlon_at(*self.mapview.to_window(*self.mapview.center))
    #         print(f"Destination set at: {self.destination}")
    #         self.selecting_origin = False
    #         self.draw_route(self.origin, self.destination)


    # def on_map_click(self, instance, location):
    #     if self.selecting_origin:
    #         if not self.origin:
    #             self.origin = location
    #             print(f"Origin set at: {self.origin}")
    #         else:
    #             self.destination = location
    #             print(f"Destination set at: {self.destination}")


    # def draw_route(self, origin, destination):
    #     if origin and destination:
    #         with self.mapview.canvas:
    #             # Set the line properties (color, width, etc.)
    #             Color(0, 0, 1)  # Blue color
    #             Line(points=[origin[0], origin[1], destination[0], destination[1]], width=3)

    #         directions = self.gmaps.directions(origin, destination, mode="driving")
    #         if not directions:
    #             print("No directions found between the locations")
    #     else:
    #         print("Please select both origin and destination first.")
 


class MapApp(App):
    def build(self):
        return MapWithMarkers()

if __name__ == '__main__':
    MapApp().run()


