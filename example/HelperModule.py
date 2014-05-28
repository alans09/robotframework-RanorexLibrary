class HelperModule(object):
    def save_base64_screenshot(self, image, path):
        fh = open(path, "wb")
        fh.write(image.decode('base64'))
        fh.close()

    def load_json_file(self, file_name):
        import json
        json_data = open(file_name).read()
        data = json.loads(json_data)
        return data
