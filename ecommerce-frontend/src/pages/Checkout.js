import { useEffect, useState } from "react";
import API from "../api";

function Checkout({ onSuccess }) {
  const [addresses, setAddresses] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAddresses();
  }, []);

  const fetchAddresses = async () => {
    try {
      const res = await API.get("addresses/");
      setAddresses(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const placeOrder = async () => {
    if (!selectedAddress) {
      alert("Please select an address");
      return;
    }

    try {
      setLoading(true);

      const res = await API.post("orders/", {
        shipping_address_id: selectedAddress,
        billing_address_id: selectedAddress,
      });

      onSuccess(res.data.order_id);
    } catch (err) {
      console.error(err);
      alert("Order failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "700px", margin: "auto" }}>
      <h2 style={{ textAlign: "center" }}>📦 Checkout</h2>

      {/* Address Section */}
      <div
        style={{
          background: "#fff",
          padding: "20px",
          borderRadius: "10px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          marginTop: "20px",
        }}
      >
        <h3>Select Delivery Address</h3>

        {addresses.length === 0 ? (
          <p>No addresses found</p>
        ) : (
          addresses.map((addr) => (
            <div
              key={addr.id}
              onClick={() => setSelectedAddress(addr.id)}
              style={{
                border:
                  selectedAddress === addr.id
                    ? "2px solid #007bff"
                    : "1px solid #ddd",
                padding: "10px",
                marginTop: "10px",
                borderRadius: "8px",
                cursor: "pointer",
                background:
                  selectedAddress === addr.id ? "#f0f8ff" : "#fff",
              }}
            >
              <p style={{ margin: 0 }}>
                <strong>{addr.name}</strong> ({addr.phone})
              </p>
              <p style={{ margin: 0 }}>
                {addr.line1}, {addr.city}
              </p>
            </div>
          ))
        )}
      </div>

      {/* Order Button */}
      <div
        style={{
          marginTop: "20px",
          textAlign: "center",
        }}
      >
        <button
          onClick={placeOrder}
          disabled={loading}
          style={{
            padding: "12px 25px",
            background: "#28a745",
            color: "#fff",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontSize: "16px",
            opacity: loading ? 0.6 : 1,
          }}
        >
          {loading ? "Placing Order..." : "Place Order"}
        </button>
      </div>
    </div>
  );
}

export default Checkout;