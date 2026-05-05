import { useState } from "react";
import API from "../api";

function Payment({ orderId }) {
  const [paymentId, setPaymentId] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const createPayment = async () => {
    try {
      setLoading(true);

      const res = await API.post("payments/create/", {
        order_id: orderId,
      });

      setPaymentId(res.data.payment_id);
      setStatus("INITIATED");
    } catch (err) {
      console.error(err);
      alert("Payment init failed");
    } finally {
      setLoading(false);
    }
  };

  const verifyPayment = async (result) => {
    try {
      setLoading(true);

      const res = await API.post("payments/verify/", {
        payment_id: paymentId,
        status: result,
      });

      setStatus(res.data.order_status);
    } catch (err) {
      console.error(err);
      alert("Payment verification failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        padding: "20px",
        maxWidth: "500px",
        margin: "auto",
      }}
    >
      <h2 style={{ textAlign: "center" }}>💳 Payment</h2>

      <div
        style={{
          background: "#fff",
          padding: "20px",
          borderRadius: "10px",
          boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
          marginTop: "20px",
          textAlign: "center",
        }}
      >
        {/* Order Info */}
        <p>
          <strong>Order ID:</strong> {orderId}
        </p>

        {/* Create Payment */}
        {!paymentId && (
          <button
            onClick={createPayment}
            disabled={loading}
            style={{
              marginTop: "10px",
              padding: "10px 20px",
              background: "#007bff",
              color: "#fff",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
              opacity: loading ? 0.6 : 1,
            }}
          >
            {loading ? "Processing..." : "Pay Now"}
          </button>
        )}

        {/* Payment Actions */}
        {paymentId && status === "INITIATED" && (
          <div style={{ marginTop: "20px" }}>
            <p>Choose payment result (demo)</p>

            <button
              onClick={() => verifyPayment("SUCCESS")}
              style={{
                marginRight: "10px",
                padding: "10px",
                background: "#28a745",
                color: "#fff",
                border: "none",
                borderRadius: "6px",
                cursor: "pointer",
              }}
            >
              ✅ Success
            </button>

            <button
              onClick={() => verifyPayment("FAILED")}
              style={{
                padding: "10px",
                background: "#dc3545",
                color: "#fff",
                border: "none",
                borderRadius: "6px",
                cursor: "pointer",
              }}
            >
              ❌ Fail
            </button>
          </div>
        )}

        {/* Status Display */}
        {status && status !== "INITIATED" && (
          <div style={{ marginTop: "20px" }}>
            <h3
              style={{
                color: status === "PAID" ? "green" : "red",
              }}
            >
              {status === "PAID"
                ? "🎉 Payment Successful!"
                : "❌ Payment Failed"}
            </h3>
          </div>
        )}
      </div>
    </div>
  );
}

export default Payment;