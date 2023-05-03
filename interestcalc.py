import streamlit as st
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np

def calculate_total_interest(price, interest_rate, loan_years, down_payment):
    loan_amount = price - down_payment
    monthly_interest_rate = (interest_rate / 100) / 12
    loan_months = loan_years * 12

    numerator = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_months)
    denominator = ((1 + monthly_interest_rate) ** loan_months) - 1
    monthly_payment = numerator / denominator

    total_amount_paid = monthly_payment * loan_months
    total_interest_paid = total_amount_paid - loan_amount

    return total_interest_paid, monthly_payment

def generate_amortization_table(price, interest_rate, loan_years, down_payment):
    loan_amount = price - down_payment
    monthly_interest_rate = (interest_rate / 100) / 12
    loan_months = loan_years * 12

    _, monthly_payment = calculate_total_interest(price, interest_rate, loan_years, down_payment)

    amortization_table = [[1,0,0,loan_amount]]
    remaining_balance = loan_amount

    for i in range(1, loan_months):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment

        amortization_table.append([i + 1, interest_payment, principal_payment, remaining_balance])

    return np.array(amortization_table)

def main():
    st.title("Car Loan Interest Calculator")

    price = st.number_input("Enter the car's price:", min_value=0.0, step=1000.0)
    interest_rate = st.number_input("Enter the annual interest rate (as a percentage):", min_value=0.0, max_value=100.0, step=0.1)
    loan_years = st.number_input("Enter the number of years for the car loan:", min_value=0, step=1)
    down_payment = st.number_input("Enter the down payment amount (if any):", min_value=0.0, step=1000.0)

    if st.button("Calculate"):
        total_interest_paid, _ = calculate_total_interest(price, interest_rate, loan_years, down_payment)
        st.write(f"The total amount of interest paid over the life of the loan is: ${total_interest_paid:.2f}")

        amortization_table = generate_amortization_table(price, interest_rate, loan_years, down_payment)
        figure = ff.create_table(amortization_table, header_values=["Month", "Interest Payment", "Principal Payment", "Remaining Balance"])
        st.plotly_chart(figure)


        # Create a line chart for Interest and Principal payments
        line_chart = go.Figure()
        line_chart.add_trace(go.Scatter(x=amortization_table[:, 0], y=amortization_table[:, 1], mode="lines", name="Interest Payment"))
        line_chart.add_trace(go.Scatter(x=amortization_table[:, 0], y=amortization_table[:, 2], mode="lines", name="Principal Payment"))
        line_chart.update_layout(title="Interest and Principal Payments Over Time", xaxis_title="Month", yaxis_title="Amount ($)")
        st.plotly_chart(line_chart)
        
        # Create a pie chart comparing total amount paid with and without interest
        loan_amount = price - down_payment
        total_amount_paid = loan_amount + total_interest_paid
        pie_chart = go.Figure(data=[go.Pie(labels=["Total Amount Paid (with Interest)", "Car Price"],
                                           values=[total_amount_paid, price],
                                           hole=0.4)])
        pie_chart.update_layout(title="Comparison of Total Amount Paid with and without Interest")
        st.plotly_chart(pie_chart)



if __name__ == "__main__":
    main()
