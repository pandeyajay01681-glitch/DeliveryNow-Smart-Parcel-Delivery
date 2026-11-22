
import streamlit as st
import pandas as pd
import os

from datetime import date, time
from database import (
    create_table,
    create_booking,
    get_booking,
    get_all_bookings,
    update_status
)

# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="DeliveryNow | Smart Logistics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_table()

# ---------------- DESIGN ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #080D1A;
    color: #F8FAFC;
}

[data-testid="stSidebar"] {
    background: #10182B;
    border-right: 1px solid #26334D;
}

.hero {
    padding: 48px 38px;
    border-radius: 24px;
    background: linear-gradient(120deg, #182B53, #43247B, #172C4D);
    border: 1px solid #5365A0;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 46px;
    font-weight: 800;
    color: white;
    margin-bottom: 8px;
}

.hero p {
    font-size: 17px;
    color: #D8E3FF;
}

.stat {
    background: #121D32;
    padding: 22px;
    border-radius: 17px;
    border: 1px solid #263650;
}

.stat h2 {
    color: #A78BFA;
    font-size: 30px;
    margin: 5px 0;
}

.stat p {
    color: #AAB8CE;
    margin: 0;
}

.section {
    font-size: 25px;
    font-weight: 750;
    margin: 22px 0 12px;
}

.stButton > button {
    background: linear-gradient(90deg, #7657F5, #A855F7);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    min-height: 45px;
}

.stButton > button:hover {
    border: 1px solid #C4B5FD;
    color: white;
}

div[data-testid="stMetric"] {
    background: #121D32;
    padding: 18px;
    border: 1px solid #263650;
    border-radius: 14px;
}

input, textarea {
    border-radius: 9px !important;
}

.footer {
    text-align: center;
    color: #8291AB;
    padding: 30px;
    border-top: 1px solid #263650;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

st.sidebar.markdown("## 📦 DeliveryNow")
st.sidebar.caption("SMART PARCEL LOGISTICS")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Home",
        "Book Delivery",
        "Track Parcel",
        "My Bookings",
        "Admin Dashboard"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Your parcels, on your schedule.")


# ---------------- HOME ----------------

if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>Deliver smarter.<br>Live better.</h1>
        <p>Book your parcel delivery at the time that works for you.
        Fast, simple and convenient.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="stat">
            <h2>01</h2>
            <p>Schedule your parcel</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="stat">
            <h2>02</h2>
            <p>Track your booking</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="stat">
            <h2>03</h2>
            <p>Stay updated</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section">Why choose DeliveryNow?</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        st.info("📅 **Flexible Scheduling**\n\nChoose your preferred delivery date and time.")

    with b:
        st.info("📍 **Easy Tracking**\n\nTrack your booking with a unique tracking ID.")

    with c:
        st.info("💳 **Transparent Pricing**\n\nSee the estimated price before booking.")

    if st.button("Book a delivery now →"):
        st.session_state["selected_page"] = "Book Delivery"
        st.rerun()


# ---------------- BOOK DELIVERY ----------------

elif page == "Book Delivery":

    st.title("📦 Schedule Your Delivery")
    st.caption("Enter your parcel details and choose your preferred time.")

    with st.form("booking_form"):

        st.subheader("Customer Information")

        customer = st.text_input("Full Name")
        phone = st.text_input("Phone Number")

        st.subheader("Delivery Information")

        col1, col2 = st.columns(2)

        with col1:
            pickup = st.text_input("Pickup Address")

        with col2:
            destination = st.text_input("Destination Address")

        package = st.selectbox(
            "Package Type",
            ["Documents", "Small Parcel", "Medium Parcel", "Large Parcel"]
        )

        weight = st.number_input(
            "Package Weight (kg)",
            min_value=0.1,
            max_value=50.0,
            value=1.0,
            step=0.5
        )

        delivery_type = st.selectbox(
            "Delivery Speed",
            ["Standard", "Express"]
        )

        st.subheader("Preferred Delivery Schedule")

        col3, col4 = st.columns(2)

        with col3:
            delivery_date = st.date_input(
                "Delivery Date",
                min_value=date.today()
            )

        with col4:
            delivery_time = st.time_input(
                "Preferred Time",
                value=time(10, 0)
            )

        # Demo pricing calculation
        base_price = 50 + (weight * 20)

        if delivery_type == "Express":
            price = base_price * 1.5
        else:
            price = base_price

        st.markdown(
            f"### Estimated Delivery Price: ₹{price:.2f}"
        )

        st.caption(
            "Demo estimate only. Actual courier rates may vary."
        )

        submitted = st.form_submit_button(
            "Confirm Delivery Booking",
            use_container_width=True
        )

        if submitted:

            if not customer.strip() or not phone.strip():
                st.error("Please enter your name and phone number.")

            elif not phone.strip().isdigit() or len(phone.strip()) != 10:
                st.error("Enter a valid 10-digit phone number.")

            elif not pickup.strip() or not destination.strip():
                st.error("Please enter both addresses.")

            elif delivery_date == date.today() and delivery_time <= time.now():
                st.error("Choose a future delivery time.")

            else:
                booking_data = {
                    "customer": customer.strip(),
                    "phone": phone.strip(),
                    "pickup": pickup.strip(),
                    "destination": destination.strip(),
                    "package": package,
                    "weight": weight,
                    "delivery_type": delivery_type,
                    "delivery_date": str(delivery_date),
                    "delivery_time": delivery_time.strftime("%H:%M"),
                    "price": price
                }

                tracking_id = create_booking(booking_data)

                st.success("Your booking has been created!")
                st.markdown(f"### Tracking ID: `{tracking_id}`")
                st.info("Save this tracking ID to check your booking status.")


# ---------------- TRACK PARCEL ----------------

elif page == "Track Parcel":

    st.title("📍 Track Your Parcel")
    st.write("Enter your booking ID below.")

    tracking_id = st.text_input("Tracking ID").strip().upper()

    if st.button("Track Now"):

        if tracking_id:
            booking = get_booking(tracking_id)

            if booking:

                st.success("Booking found!")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Tracking ID", booking["tracking_id"])
                    st.metric("Status", booking["status"])

                with col2:
                    st.metric("Delivery Type", booking["delivery_type"])
                    st.metric("Price", f"₹{booking['price']:.2f}")

                st.markdown("### Delivery Details")

                st.write("**Customer:**", booking["customer"])
                st.write("**Pickup:**", booking["pickup"])
                st.write("**Destination:**", booking["destination"])
                st.write("**Scheduled Date:**", booking["delivery_date"])
                st.write("**Scheduled Time:**", booking["delivery_time"])

                stages = [
                    "Booked",
                    "Picked Up",
                    "In Transit",
                    "Out for Delivery",
                    "Delivered"
                ]

                current_stage = booking["status"]

                if current_stage in stages:
                    st.progress(
                        (stages.index(current_stage) + 1) / len(stages)
                    )

                st.write(" → ".join(stages))

            else:
                st.error("No booking found. Please check your tracking ID.")

        else:
            st.warning("Please enter your tracking ID.")


# ---------------- MY BOOKINGS ----------------

elif page == "My Bookings":

    st.title("📋 Booking History")

    tracking_id = st.text_input("Enter your Tracking ID")

    if st.button("Find Booking"):

        booking = get_booking(tracking_id.strip().upper())

        if booking:
            st.success("Booking found!")

            df = pd.DataFrame([booking])
            st.dataframe(df, use_container_width=True)

        else:
            st.error("Booking not found.")


# ---------------- ADMIN DASHBOARD ----------------

elif page == "Admin Dashboard":

    st.title("⚙️ Admin Dashboard")
    st.caption("Restricted management area.")

    admin_password = st.text_input(
        "Admin Password",
        type="password"
    )

    configured_password = os.environ.get("ADMIN_PASSWORD", "")

    try:
        configured_password = st.secrets.get(
            "ADMIN_PASSWORD",
            configured_password
        )
    except Exception:
        pass

    if not configured_password:
        st.warning(
            "Admin access is not configured. Set ADMIN_PASSWORD "
            "in your deployment secrets."
        )

    elif admin_password and admin_password == configured_password:

        bookings = get_all_bookings()
        df = pd.DataFrame(bookings)

        total = len(bookings)
        delivered = sum(
            b["status"] == "Delivered" for b in bookings
        )
        pending = total - delivered
        revenue = sum(b["price"] for b in bookings)

        a, b, c, d = st.columns(4)

        a.metric("Total Bookings", total)
        b.metric("Delivered", delivered)
        c.metric("Pending", pending)
        d.metric("Booking Value", f"₹{revenue:.2f}")

        st.subheader("All Bookings")

        if not df.empty:
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Download Booking Report",
                csv,
                "delivery_report.csv",
                "text/csv"
            )

            st.subheader("Update Delivery Status")

            selected_id = st.selectbox(
                "Select Tracking ID",
                df["tracking_id"].tolist()
            )

            new_status = st.selectbox(
                "New Status",
                [
                    "Booked",
                    "Picked Up",
                    "In Transit",
                    "Out for Delivery",
                    "Delivered"
                ]
            )

            if st.button("Update Status"):
                update_status(selected_id, new_status)
                st.success("Delivery status updated!")
                st.rerun()

        else:
            st.info("No bookings available yet.")

    elif admin_password:
        st.error("Incorrect admin password.")


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    <h3>📦 DeliveryNow</h3>
    Smart delivery. Your schedule. Your convenience.<br>
    Built with Python and Streamlit.
</div>
""", unsafe_allow_html=True)
