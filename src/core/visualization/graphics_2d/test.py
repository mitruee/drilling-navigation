from horizontal_wells import *
import matplotlib.pyplot as plt


fig1, axes1 = plt.subplots(figsize=(9, 6))

directional_profile = DirectionalProfilesGraphic(TwoInterval(1678, 900, 80), axes1)
horizontal_profile = HorizontalProfilesGraphic(Tangential(1678, 900, 80, 400), axes1)

directional_profile.draw()
horizontal_profile.draw()
plt.show()


fig2, axes2 = plt.subplots(figsize=(9, 6))

directional_profile = DirectionalProfilesGraphic(TangentialFourInterval(1678, 900, 40, 30, 382, 1900), axes2)
horizontal_profile = HorizontalProfilesGraphic(Ascending(1678, 900, 70, 400, 20), axes2)

directional_profile.draw()
horizontal_profile.draw()
plt.show()


fig3, axes3 = plt.subplots(figsize=(9, 6))

directional_profile = DirectionalProfilesGraphic(ThreeInterval(1600, 400, 30, 40, 400), axes3)
horizontal_profile = HorizontalProfilesGraphic(Descending(1600, 400, 70, 100, 20), axes3)

directional_profile.draw()
horizontal_profile.draw()
plt.show()


fig4, axes4 = plt.subplots(figsize=(9, 6))

directional_profile = DirectionalProfilesGraphic(TangentialFiveInterval(2000, 900, 50, 30, 382, 1900, 40, 200), axes4)
horizontal_profile = HorizontalProfilesGraphic(Descending(2000, 900, 55, 100, 20), axes4)

directional_profile.draw()
horizontal_profile.draw()
plt.show()


fig5, axes5 = plt.subplots(figsize=(9, 6))

directional_profile = DirectionalProfilesGraphic(FourInterval(2000, 900, 50, 30, 382, 500, 40), axes5)
horizontal_profile = HorizontalProfilesGraphic(Descending(2000, 900, 45, 400, 20), axes5)

directional_profile.draw()
horizontal_profile.draw()
plt.show()