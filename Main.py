from skimage.io import imread, imsave
from telegram.ext import *
import os
import time

from UniformQuantization import Uniform_quantization
from MedianCut import Median_cut
from KMeans import KMeans
from VectorQuantization import Vector_quantization
from OCTree import OCTree

from config import TOKEN

img = [[[]]]
num_regions = 2
dept = 4
K_num = 16
max_iters = 5
cb_size=16
epsilon_value=0.0005
d=1
block_width_value = 8
block_height_value = 8
block_value = (20, 10, d)
palette_value = 38

photo_name = "img.jpg"
res_name = "res.jpg"
PHOTO, NUMBER_OF_REGIONS, DEPTH, K, MAX_ITERATION, CODEBOOK_SIZE, EPSILON, BLOCK_WIDTH, BLOCK_HEIGHT, PALETTE = range(10)
type_of_quantization = 0

async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!"
    )
    await update.message.reply_text("This is bot for image compression with clusterization.\n"
                                    "Type /help to get list of commands.")

async def help(update, context):
    await update.message.reply_text("Commands:\n"
                                    "/uniform_quantization - for quantization with range of colors split. "
                                    "After this command bot ask about image and number of regions for color.\n"
                                    "/median_cut - quantization with split on median in color with bigest variety. "
                                    "Need: image, depth(how many splits will be produced.\n"
                                    "/kmeans - for quantization with k-means clustering. "
                                    "Need: image, number of clusters and number of iterations.\n"
                                    "/kmeans_parcs - k-means with PARCS. "
                                    "Need: image.\n"
                                    "/vector_quantization - for block quantization. "
                                    "Need: image, coddebook size, epsilon for accuracy and block width and height.\n"
                                    "/kmeans - for quantization with graph trees. "
                                    "Need: image and palette.\n"
                                    "Also can quit from command with /cancel.")

###############################################################################################

async def uniform_quantization(update, context):
    global type_of_quantization
    type_of_quantization = NUMBER_OF_REGIONS
    await update.message.reply_text("Send image")
    return PHOTO

async def number_of_regions(update, context):
    num_regions = int(update.message.text)

    await update.message.reply_text("Wait for result")

    res_img = Uniform_quantization(img, num_regions)
    imsave(res_name, res_img)

    await update.message.reply_text("Result:")
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(res_name, 'rb'))

    return ConversationHandler.END

###############################################################################################

async def median_cut(update, context):
    global type_of_quantization
    type_of_quantization = DEPTH
    await update.message.reply_text("Send image")
    return PHOTO

async def depth(update, context):
    depth = int(update.message.text)

    await update.message.reply_text("Wait for result")

    res_img = Median_cut(img, depth)
    imsave(res_name, res_img)

    await update.message.reply_text("Result:")
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(res_name, 'rb'))

    return ConversationHandler.END

###############################################################################################

async def kmeans(update, context):
    global type_of_quantization
    type_of_quantization = K
    await update.message.reply_text("Send image")
    return PHOTO

async def k(update, context):
    global K_num
    K_num = int(update.message.text)
    await update.message.reply_text("Max iteration")
    return MAX_ITERATION

async def max_iter(update, context):
    max_iters = int(update.message.text)

    await update.message.reply_text("Wait for result")

    res_img = KMeans(img, K_num, max_iters)
    imsave(res_name, res_img)

    await update.message.reply_text("Result:")
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(res_name, 'rb'))

    return ConversationHandler.END

###############################################################################################

async def vector_quantization(update, context):
    global type_of_quantization
    type_of_quantization = CODEBOOK_SIZE
    await update.message.reply_text("Send image")
    return PHOTO

async def codebook_size(update, context):
    global cb_size
    cb_size = int(update.message.text)
    await update.message.reply_text("Epsilon")
    return EPSILON

async def epsilon(update, context):
    global epsilon_value
    epsilon_value = float(update.message.text)
    await update.message.reply_text("Block width")
    return BLOCK_WIDTH

async def block_width(update, context):
    global block_width_value
    block_width_value = int(update.message.text)
    await update.message.reply_text("Block height")
    return BLOCK_HEIGHT

async def block_height(update, context):
    block_height_value = int(update.message.text)

    d=1
    if (len(img.shape) > 2): d = img.shape[2]
    block = (block_width_value, block_height_value, d)

    await update.message.reply_text("Wait for result")

    res_img = Vector_quantization(img, cb_size, epsilon_value, block)
    imsave(res_name, res_img)
    
    await update.message.reply_text("Result:")
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(res_name, 'rb'))

    return ConversationHandler.END

###############################################################################################

async def octree(update, context):
    global type_of_quantization
    type_of_quantization = PALETTE
    await update.message.reply_text("Send image")
    return PHOTO

async def palette(update, context):
    palette_value = int(update.message.text)

    await update.message.reply_text("Wait for result")

    res_img = OCTree(img, palette_value)
    imsave(res_name, res_img)

    await update.message.reply_text("Result:")
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(res_name, 'rb'))

    return ConversationHandler.END

###############################################################################################

async def kmp(update, context):
    await update.message.reply_text("Send image")
    return PHOTO

async def parcs(update, context):
    global img
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive(photo_name)
    img = imread(photo_name)

    await update.message.reply_text("Wait for result")
    
    input_name = "out/Input.jpg"
    res_name = "out/Res.jpg"

    imsave(input_name, img)

    if os.path.exists(res_name):
        os.remove(res_name)

    os.system("make")
    
    while not os.path.exists(res_name):
        time.sleep(1)

    await update.message.reply_text("Result:")
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(res_name, 'rb'))

    return ConversationHandler.END

###############################################################################################

async def photo(update, context):
    global img
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive(photo_name)
    img = imread(photo_name)

    text = ""
    if(type_of_quantization == NUMBER_OF_REGIONS): text = "Number of regions"
    elif(type_of_quantization == DEPTH): text = "Depth"
    elif(type_of_quantization == K): text = "Number of cluster"
    elif(type_of_quantization == CODEBOOK_SIZE): text = "Codebook size"
    elif(type_of_quantization == PALETTE): text = "Palette"

    await update.message.reply_text(text)

    return type_of_quantization

async def send_photo(update, context):
    await update.message.reply_text("Send image")

async def send_integer(update, context):
    await update.message.reply_text("Send integer")

async def send_float(update, context):
    await update.message.reply_text("Send float")

async def cancel(update, context):
    await update.message.reply_text("Operation canceled")
    return ConversationHandler.END

###############################################################################################

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    uq_handler = ConversationHandler(
        entry_points=[CommandHandler("uniform_quantization", uniform_quantization)],
        states={
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_photo)],
            NUMBER_OF_REGIONS: [MessageHandler(filters.Regex("^[0-9]+$"), number_of_regions), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_integer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(uq_handler)

    mc_handler = ConversationHandler(
        entry_points=[CommandHandler("median_cut", median_cut)],
        states={
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_photo)],
            DEPTH: [MessageHandler(filters.Regex("^[0-9]+$"), depth), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_integer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(mc_handler)

    km_handler = ConversationHandler(
        entry_points=[CommandHandler("kmeans", kmeans)],
        states={
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_photo)],
            K: [MessageHandler(filters.Regex("^[0-9]+$"), k), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_integer)],
            MAX_ITERATION: [MessageHandler(filters.Regex("^[0-9]+$"), max_iter), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_integer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(km_handler)

    kmp_handler = ConversationHandler(
        entry_points=[CommandHandler("kmeans_parcs", kmp)],
        states={
            PHOTO: [MessageHandler(filters.PHOTO, parcs), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_photo)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(kmp_handler)
    
    vq_handler = ConversationHandler(
        entry_points=[CommandHandler("vector_quantization", vector_quantization)],
        states={
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_photo)],
            CODEBOOK_SIZE: [MessageHandler(filters.Regex("^[0-9]+$"), codebook_size), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_integer)],
            EPSILON: [MessageHandler(filters.Regex("^0.[0-9]+$"), epsilon), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_float)],
            BLOCK_WIDTH: [MessageHandler(filters.Regex("^[0-9]+$"), block_width), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_integer)],
            BLOCK_HEIGHT: [MessageHandler(filters.Regex("^[0-9]+$"), block_height), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_integer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(vq_handler)

    ot_handler = ConversationHandler(
        entry_points=[CommandHandler("octree", octree)],
        states={
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_photo)],
            PALETTE: [MessageHandler(filters.Regex("^[0-9]+$"), palette), CommandHandler("cancel", cancel), MessageHandler(filters.ALL, send_integer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(ot_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
