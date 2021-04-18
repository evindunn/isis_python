from isis.base import Cube
from time import sleep

cb = Cube("/home/edunn/Desktop/ctx-process/P22_009808_1436_XI_36S210W.cub")
print("Is open:                            {}".format(cb.is_open()))
print("Is projected:                       {}".format(cb.is_projected()))
print("Is read only:                       {}".format(cb.is_read_only()))
print("Is read/write:                      {}".format(cb.is_read_write()))
print("Labels attached:                    {}".format(cb.labels_attached()))
print("Band Count:                         {}".format(cb.band_count()))
print("Base:                               {}".format(cb.base()))
print("Byte Order:                         {}".format(cb.byte_order()))
# print("External Cube File Name: {}".format(cb.external_cube_file_name()))
print("File Name:                          {}".format(cb.file_name()))
print("Label Size:                         {}".format(cb.label_size(True)))
print("Line Count:                         {}".format(cb.line_count()))
print("Multiplier:                         {}".format(cb.multiplier()))
print("Sample Count:                       {}".format(cb.sample_count()))
print("Stores DN data:                     {}".format(cb.stores_dn_data()))
print("Has group 'NonExistent':            {}".format(cb.has_group("NonExistent")))
print("Has table 'Ctx Prefix Dark Pixels': {}".format(cb.has_table("Ctx Prefix Dark Pixels")))

print()
print("Label:")
print("======")
for line in str(cb.label()).split("\n"):
    print(line)
    sleep(0.5)
