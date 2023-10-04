import yaml
import time

skrapbuk_start_time = 1703462399

class Config:
    def __init__(self, file_path):
        self.file_path = file_path

        with open(self.file_path, 'r') as  file:
            self.config = yaml.safe_load(file)

    def find_value(self, key):
        return self.config.get('discord', {}).get(key, None)

    def get_admins(self):
        return list(self.config.get('discord', {}).get('admins', {}).values())

    def get_countdown(self):
        current_time = int(time.time())
        time_difference = max(skrapbuk_start_time - current_time, 0)

        days = time_difference // (24 * 3600)
        time_difference %= (24 * 3600)
        hours = time_difference // 3600
        time_difference %= 3600
        minutes = time_difference // 60
        seconds = time_difference % 60

        return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"