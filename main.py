# This is a sample Python script.
from time import sleep

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import uiautomator2 as u2


class DeviceControl(object):

    def __init__(self, device_id):
        self.item_info_classname = None
        self.item_time_resource_id = None
        self.item_size_resource_id = None
        self.item_name_resource_id = None
        self.item_classname = None
        self.device_id = device_id
        self.d = u2.connect(self.device_id)
        self.r_personal_space = None
        self.r_file_view = None
        self.classname = None

        self.setup()

    def setup(self):
        self.r_personal_space = self.d(text="私人专属空间")
        self.r_file_view = self.d(resourceId="com.lenovo.smartpan:id/recycler_view")
        self.item_classname = 'android.widget.RelativeLayout'
        self.item_info_classname = 'android.widget.LinearLayout'

        self.item_name_resource_id = 'com.lenovo.smartpan:id/txt_name'
        self.item_time_resource_id = 'com.lenovo.smartpan:id/txt_time'
        self.item_size_resource_id = 'com.lenovo.smartpan:id/txt_size'

    def swipe(self, step=1):
        for i in range(step):
            self.d.swipe_ext('up', 0.7)
            sleep(1)

    def list_files_single_page(self):

        file_list = {}
        count = self.r_file_view.info['childCount']
        for i in range(count):
            item_card = self.r_file_view.child(className=self.item_classname, index=i).child(
                className=self.item_classname)
            item_name = item_card.child(resourceId=self.item_name_resource_id).get_text()
            item_time = item_card.child(resourceId=self.item_time_resource_id).get_text()
            item_size = -1
            if item_card.child(resourceId=self.item_size_resource_id).exists:
                item_size = item_card.child(resourceId=self.item_size_resource_id).get_text()

            file_list[item_name] = {'time': item_time,
                                    'size': item_size}

        print(file_list)

    def list_files_multi_page(self):

        file_list = {}
        page = 0
        card_bounds = \
            self.r_file_view.child(className=self.item_classname, index=0).child(className=self.item_classname).info[
                'visibleBounds']
        reference_height = card_bounds['bottom'] - card_bounds['top']
        while True:
            file_count = len(file_list)
            count = self.r_file_view.info['childCount']
            for i in range(count):
                item_card = self.r_file_view.child(className=self.item_classname, index=i).child(
                    className=self.item_classname)
                bounds = item_card.info['visibleBounds']
                if bounds['bottom'] - bounds['top'] < reference_height:
                    continue

                item_name = item_card.child(resourceId=self.item_name_resource_id).get_text()
                item_time = item_card.child(resourceId=self.item_time_resource_id).get_text()
                item_size = -1
                if item_card.child(resourceId=self.item_size_resource_id).exists:
                    item_size = item_card.child(resourceId=self.item_size_resource_id).get_text()

                file_list[item_name] = {'time': item_time,
                                        'size': item_size}
            if len(file_list) == file_count:
                break
            self.swipe()

        print(file_list)



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    device_control = DeviceControl('19473177')
    device_control.list_files_multi_page()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
