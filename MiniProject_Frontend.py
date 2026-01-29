from tkinter import *
import tkinter.messagebox
import MiniProject_Backend

# Initialize database and trigger
MiniProject_Backend.MovieData()
MiniProject_Backend.create_trigger()
#

class Movie:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Movie Ticket Booking System")
        self.root.geometry("1350x750+0+0")
        self.root.config(bg="black")

        # ================= VARIABLES =================
        self.Movie_ID = StringVar()
        self.Movie_Name = StringVar()
        self.Release_Date = StringVar()
        self.Director = StringVar()
        self.Cast = StringVar()
        self.Budget = StringVar()
        self.Duration = StringVar()
        self.Rating = StringVar()

        self.Show_ID = StringVar()
        self.Customer_Name = StringVar()
        self.Seats_To_Book = StringVar()

        # ================= FUNCTIONS =================
        def iExit():
            if tkinter.messagebox.askyesno(
                "Online Movie Ticket Booking System", "Are you sure?"
            ):
                root.destroy()

        def clcdata():
            self.Movie_ID.set("")
            self.Movie_Name.set("")
            self.Release_Date.set("")
            self.Director.set("")
            self.Cast.set("")
            self.Budget.set("")
            self.Duration.set("")
            self.Rating.set("")

        def adddata():
            MiniProject_Backend.AddMovieRec(
                self.Movie_ID.get(),
                self.Movie_Name.get(),
                self.Release_Date.get(),
                self.Director.get(),
                self.Cast.get(),
                self.Budget.get(),
                self.Duration.get(),
                self.Rating.get()
            )
            disdata()

        def disdata():
            MovieList.delete(0, END)
            for row in MiniProject_Backend.ViewMovieData():
                MovieList.insert(END, row)

        def movierec(event):
            if not MovieList.curselection():
                return
            index = MovieList.curselection()[0]
            data = MovieList.get(index)

            if len(data) >= 9:
                self.Movie_ID.set(data[1])
                self.Movie_Name.set(data[2])
                self.Release_Date.set(data[3])
                self.Director.set(data[4])
                self.Cast.set(data[5])
                self.Budget.set(data[6])
                self.Duration.set(data[7])
                self.Rating.set(data[8])

        def deldata():
            if MovieList.curselection():
                index = MovieList.curselection()[0]
                data = MovieList.get(index)
                MiniProject_Backend.DeleteMovieRec(data[0])
                disdata()

        def updata():
            if MovieList.curselection():
                index = MovieList.curselection()[0]
                data = MovieList.get(index)
                MiniProject_Backend.DeleteMovieRec(data[0])
                adddata()

        # ================= BOOKING FUNCTIONS =================
        def view_shows():
            MovieList.delete(0, END)
            for s in MiniProject_Backend.ViewShows():
                MovieList.insert(END, s)

        def check_seats():
            seats = MiniProject_Backend.CheckSeats(int(self.Show_ID.get()))
            tkinter.messagebox.showinfo(
                "Seat Availability", f"Available Seats: {seats}"
            )

        def book_ticket():
            try:
                seats_left = MiniProject_Backend.CheckSeats(
                    int(self.Show_ID.get())
                )

                if seats_left <= 0:
                    tkinter.messagebox.showerror(
                        "Sold Out", "Seats not available!"
                    )
                    return

                MiniProject_Backend.BookTicket(
                    int(self.Show_ID.get()),
                    self.Customer_Name.get(),
                    int(self.Seats_To_Book.get())
                )

                tkinter.messagebox.showinfo(
                    "Success", "Ticket Booked Successfully"
                )
                view_shows()

            except Exception as e:
                tkinter.messagebox.showerror(
                    "Booking Failed", str(e)
                )

        # ================= FRAMES =================
        MainFrame = Frame(self.root, bg="black")
        MainFrame.grid()

        TFrame = Frame(
            MainFrame, bd=5, padx=54, pady=8,
            bg="black", relief=RIDGE
        )
        TFrame.pack(side=TOP)

        self.lblTitle = Label(
            TFrame, font=('Arial', 40, 'bold'),
            text="ONLINE MOVIE TICKET BOOKING SYSTEM",
            bg="black", fg="orange"
        )
        self.lblTitle.grid()

        BFrame = Frame(
            MainFrame, bd=2, width=1350,
            height=70, padx=18, pady=10,
            bg="black", relief=RIDGE
        )
        BFrame.pack(side=BOTTOM)

        DFrame = Frame(
            MainFrame, bd=2, width=1300,
            height=400, padx=20, pady=20,
            bg="black", relief=RIDGE
        )
        DFrame.pack(side=BOTTOM)

        DFrameL = LabelFrame(
            DFrame, bd=2, width=1000, height=600,
            padx=20, bg="black", relief=RIDGE,
            font=('Arial', 20, 'bold'),
            text="Movie Info", fg="white"
        )
        DFrameL.pack(side=LEFT)

        DFrameR = LabelFrame(
            DFrame, bd=2, width=450, height=300,
            padx=31, pady=3, bg="black",
            relief=RIDGE, font=('Arial', 20, 'bold'),
            text="Movie / Show Details", fg="white"
        )
        DFrameR.pack(side=RIGHT)

        # ================= LABELS & ENTRY =================
        labels = [
            ("Movie ID", self.Movie_ID),
            ("Movie Name", self.Movie_Name),
            ("Release Date", self.Release_Date),
            ("Director", self.Director),
            ("Cast", self.Cast),
            ("Budget", self.Budget),
            ("Duration", self.Duration),
            ("Rating", self.Rating)
        ]

        for i, (text, var) in enumerate(labels):
            Label(
                DFrameL, font=('Arial', 18, 'bold'),
                text=text, bg="black", fg="orange"
            ).grid(row=i, column=0, sticky=W)

            Entry(
                DFrameL, font=('Arial', 18),
                textvariable=var, width=39
            ).grid(row=i, column=1)

        # ================= LISTBOX =================
        sb = Scrollbar(DFrameR)
        sb.grid(row=0, column=1, sticky='ns')

        MovieList = Listbox(
            DFrameR, width=41, height=16,
            font=('Arial', 12, 'bold'),
            bg="black", fg="white",
            yscrollcommand=sb.set
        )
        MovieList.bind('<<ListboxSelect>>', movierec)
        MovieList.grid(row=0, column=0, padx=8)
        sb.config(command=MovieList.yview)

        # ================= BUTTONS =================
        self.btnadd = Button(
            BFrame, text="Add New",
            font=('Arial', 16, 'bold'),
            width=10, bg="orange",
            command=adddata
        )
        self.btnadd.grid(row=0, column=0)

        self.btndis = Button(
            BFrame, text="Display",
            font=('Arial', 16, 'bold'),
            width=10, bg="orange",
            command=disdata
        )
        self.btndis.grid(row=0, column=1)

        self.btnclc = Button(
            BFrame, text="Clear",
            font=('Arial', 16, 'bold'),
            width=10, bg="orange",
            command=clcdata
        )
        self.btnclc.grid(row=0, column=2)

        self.btndel = Button(
            BFrame, text="Delete",
            font=('Arial', 16, 'bold'),
            width=10, bg="orange",
            command=deldata
        )
        self.btndel.grid(row=0, column=3)

        self.btnup = Button(
            BFrame, text="Update",
            font=('Arial', 16, 'bold'),
            width=10, bg="orange",
            command=updata
        )
        self.btnup.grid(row=0, column=4)

        self.btnx = Button(
            BFrame, text="Exit",
            font=('Arial', 16, 'bold'),
            width=10, bg="orange",
            command=iExit
        )
        self.btnx.grid(row=0, column=5)

        # ================= BOOKING SECTION =================
        BookingFrame = LabelFrame(
            MainFrame, text="Ticket Booking",
            font=('Arial', 18, 'bold'),
            bg="black", fg="white",
            padx=20, pady=10
        )
        BookingFrame.pack(side=BOTTOM)

        Label(
            BookingFrame, text="Show ID",
            bg="black", fg="orange"
        ).grid(row=0, column=0)

        Entry(
            BookingFrame,
            textvariable=self.Show_ID
        ).grid(row=0, column=1)

        Label(
            BookingFrame, text="Customer Name",
            bg="black", fg="orange"
        ).grid(row=0, column=2)

        Entry(
            BookingFrame,
            textvariable=self.Customer_Name
        ).grid(row=0, column=3)

        Label(
            BookingFrame, text="Seats",
            bg="black", fg="orange"
        ).grid(row=0, column=4)

        Entry(
            BookingFrame,
            textvariable=self.Seats_To_Book
        ).grid(row=0, column=5)

        self.btnViewShows = Button(
            BookingFrame, text="View Shows",
            bg="orange", command=view_shows
        )
        self.btnViewShows.grid(row=1, column=1, pady=10)

        self.btnCheckSeats = Button(
            BookingFrame, text="Check Seats",
            bg="orange", command=check_seats
        )
        self.btnCheckSeats.grid(row=1, column=3, pady=10)

        self.btnBook = Button(
            BookingFrame, text="Book Ticket",
            bg="orange", command=book_ticket
        )
        self.btnBook.grid(row=1, column=5, pady=10)


if __name__ == "__main__":
    root = Tk()
    Movie(root)
    root.mainloop()