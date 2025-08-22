from src.core.visualization.graphics_2d.horizontal_wells import *


fig1, axes1 = plt.subplots(figsize=(9, 6))

directional_profile = DirectionalProfilesGraphic(TangentialFourInterval(1678, 900, 40, 30, 382, 1900), axes1)
horizontal_profile = HorizontalProfilesGraphic(Descending(1678, 900, 70, 400, 20), axes1)

directional_profile.draw()
horizontal_profile.draw()
plt.show()


fig2, axes2 = plt.subplots(figsize=(9, 6))

directional_profile = DirectionalProfilesGraphic(ThreeInterval(1600, 400, 30, 40, 400), axes2)
horizontal_profile = HorizontalProfilesGraphic(Descending(1600, 400, 70, 100, 20), axes2)

directional_profile.draw()
horizontal_profile.draw()
plt.show()