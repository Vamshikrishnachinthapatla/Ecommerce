import { useEffect, useState } from "react";
import API from "../api";

function Cart({ onCheckout }) {
  const [cart, setCart] = useState(null);

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const res = await API.get("cart/");
      setCart(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const removeItem = async (itemId) => {
    try {
      await API.post("cart/remove/", {
        item_id: itemId,
      });
      fetchCart();
    } catch (err) {
      console.error(err);
    }
  };

  if (!cart) return <p style={{ padding: "20px" }}>Loading...</p>;

  const total = cart.items.reduce(
    (sum, item) => sum + parseFloat(item.price) * item.quantity,
    0
  );

  return (
    <div style={{ padding: "20px", maxWidth: "700px", margin: "auto" }}>
      <h2 style={{ textAlign: "center" }}>🛒 Your Cart</h2>

      {cart.items.length === 0 ? (
        <p style={{ textAlign: "center" }}>Cart is empty</p>
      ) : (
        <>
          {cart.items.map((item) => (
            <div
              key={item.id}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                background: "#fff",
                padding: "15px",
                margin: "10px 0",
                borderRadius: "10px",
                boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
              }}
            >
              <div>
                <h4 style={{ margin: "0" }}>{item.product_name}</h4>
                <p style={{ margin: "5px 0" }}>₹ {item.price}</p>
                <p style={{ margin: "5px 0" }}>
                  Qty: <strong>{item.quantity}</strong>
                </p>
              </div>

              <button
                onClick={() => removeItem(item.id)}
                style={{
                  background: "#dc3545",
                  color: "#fff",
                  border: "none",
                  padding: "8px 12px",
                  borderRadius: "5px",
                  cursor: "pointer",
                }}
              >
                Remove
              </button>
            </div>
          ))}

          {/* Total Section */}
          <div
            style={{
              marginTop: "20px",
              padding: "15px",
              background: "#fff",
              borderRadius: "10px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
              textAlign: "center",
            }}
          >
            <h3>Total: ₹ {total.toFixed(2)}</h3>

            <button
              onClick={onCheckout}
              style={{
                marginTop: "10px",
                background: "#28a745",
                color: "#fff",
                border: "none",
                padding: "10px 20px",
                borderRadius: "5px",
                cursor: "pointer",
                fontSize: "16px",
              }}
            >
              Proceed to Checkout
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default Cart;