# from PIL import ImageOps, Image as Img
# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# User = get_user_model()
#
#
# @receiver(post_save, sender=User)
# def resize_uploaded_image(sender, instance, **kwargs):
#     img = Img.open(instance.picture.path)
#     # Means it is a rectangular
#     if img.width > img.height:
#         if img.width <= 1000:
#             pass
#         elif img.width > 1000:
#             # So as to maintain Aspect Ratio
#             new_width = 1000
#             new_height = ((new_width / img.width) * img.height)
#             img = img.resize((int(new_width), int(new_height)))
#             img.save(instance.picture.path, format=img.format, quality=60)
#         else:
#             img.save(instance.picture.path, format=img.format, quality=60)
#     # square
#     else:
#         if img.height <= 1000:
#             pass
#         else:
#             # So as to maintain Aspect Ratio
#             new_height = 1000
#             new_width = ((new_height / img.height) * img.width)
#             size = (int(new_width), int(new_height))
#             img.resize(size)
#             bg_size = (1500, 1000)
#             img = ImageOps.fit(img, bg_size, Img.ANTIALIAS, centering=(0.5, 0.5))
#             img.save(instance.picture.path, format=img.format, quality=60)
#
#
# @receiver(post_save, sender=User)
# def resize_uploaded_header_image(sender, instance, **kwargs):
#     img = Img.open(instance.header_image.path)
#     # Means it is a rectangular
#     if img.width > img.height:
#         if img.width <= 1000:
#             pass
#         elif img.width > 1000:
#             # So as to maintain Aspect Ratio
#             new_width = 1000
#             new_height = ((new_width / img.width) * img.height)
#             img = img.resize((int(new_width), int(new_height)))
#             img.save(instance.header_image.path, format=img.format, quality=60)
#         else:
#             img.save(instance.header_image.path, format=img.format, quality=60)
#     # square
#     else:
#         if img.height <= 1000:
#             pass
#         else:
#             # So as to maintain Aspect Ratio
#             new_height = 1000
#             new_width = ((new_height / img.height) * img.width)
#             size = (int(new_width), int(new_height))
#             img.resize(size)
#             bg_size = (1500, 1000)
#             img = ImageOps.fit(img, bg_size, Img.ANTIALIAS, centering=(0.5, 0.5))
#             img.save(instance.header_image.path, format=img.format, quality=60)
#
#
