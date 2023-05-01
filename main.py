import sys
import os
from os import listdir
from os.path import isfile, join
import shutil


def main(iracing_paint_path, blue_cars_path):
    print("Swapping everyone's car to blue...")
    print(f"iRacing Paint folder: {iracing_paint_path}")
    print(f"Blue Car TGA folder: {blue_cars_path}")

    blue_car_filenames = [f for f in listdir(blue_cars_path) if isfile(join(blue_cars_path, f))]
    for bcf in blue_car_filenames:
        car_name = bcf.split('_')[1].split('.')[0]
        car_paint_folder = os.path.join(iracing_paint_path, car_name)
        print(f"Car: {car_name}")
        print(f"iRacing paint folder: {car_paint_folder}")

        inter_car_paint_files_in_iracing = [f for f in listdir(car_paint_folder) if isfile(join(car_paint_folder, f))]
        car_paint_files_in_iracing = []
        for pf in inter_car_paint_files_in_iracing:
            if pf.endswith('.tga'):
                car_paint_files_in_iracing.append(pf)

        for pf in car_paint_files_in_iracing:
            user_id = pf.split('_')[-1].split('.tga')[0]
            is_team_car = "team" in pf

            car_file_prefix = "car_"
            if is_team_car:
                car_file_prefix = "car_team_"

            try:
                int(user_id)
                pass
            except ValueError:
                print(f"{user_id} is not a userid. Skipping")
                continue

            blue_car_paint_file = f'blue_{car_name}.tga'
            blue_car_paint_path = os.path.join(blue_cars_path, blue_car_paint_file)
            iracing_paint_filename = f'{car_file_prefix}{user_id}.tga'
            car_paint_path = os.path.join(car_paint_folder, iracing_paint_filename)
            temp_blue_car_paint_path = os.path.join(car_paint_folder, blue_car_paint_file)

            print(f"Swapping paint for userid: {user_id}:")
            print(f"\tOriginal: {car_paint_path}")
            print(f"\tNew Paint File: {blue_car_paint_path}")

            print("\n\tCopying new car paint file...")
            shutil.copy(blue_car_paint_path, car_paint_folder)
            print(f"\tCopied temp blue car paint file: {temp_blue_car_paint_path}")
            print(f"\tDeleting original paint file...")
            os.remove(car_paint_path)
            print(f"\tRenaming new car paint file to {iracing_paint_filename}")
            os.rename(temp_blue_car_paint_path, car_paint_path)
            print(f"\tDeleting temp blue paint file...")
            print("Done.")

        print(f"Deleting any spec map files for this {car_name}")
        for pf in inter_car_paint_files_in_iracing:
            if pf.endswith('.mip'):
                os.remove(os.path.join(car_paint_folder, pf))


args = sys.argv
main(args[1], args[2])
