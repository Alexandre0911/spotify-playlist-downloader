import customtkinter
import songDownloader



def main():
    urlVar = urlEntry.get()

    if len(urlVar) == 0:
        progressLabel.configure(require_redraw=True, text="We Need A Spotify Playlist Link!")
    else:
        progressLabel.configure(require_redraw=True, text="Started Downloading Songs!")
        songDownloader.readPlaylistFile(urlVar)
        progressLabel.configure(require_redraw=True, text="Finished Downloading Songs!")



# Set The Theme And Color Options
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")



root = customtkinter.CTk()
root.title("Spotify Playlist Downloader")
root.iconbitmap("icon.ico")
root.geometry("450x200")
root.resizable(False, False)



urlEntry = customtkinter.CTkEntry(root, placeholder_text="Spotify Playlist URL", width=400, font=('Arial', 10))
urlEntry.pack(pady=20)

downloadButton = customtkinter.CTkButton(root, text="Download", command=main)
downloadButton.pack(pady=20)

progressLabel = customtkinter.CTkLabel(root, text="Click The Button To Start Downloading")
progressLabel.pack(pady=20)



root.mainloop()