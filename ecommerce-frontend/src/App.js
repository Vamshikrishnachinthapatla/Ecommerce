import React, { useEffect, useState } from "react";
import API from "./api";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import Payment from "./pages/Payment";
import "./App.css";

function App() {
  const [products, setProducts] = useState([]);
  const [page, setPage] = useState("products");
  const [orderId, setOrderId] = useState(null);
  const [authPage, setAuthPage] = useState("login"); // 🔥 login/register toggle
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  useEffect(() => {
    if (isLoggedIn && page === "products") {
      fetchProducts();
    }
  }, [isLoggedIn, page]);

  const fetchProducts = async () => {
    try {
      const res = await API.get("products/");
      setProducts(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const addToCart = async (productId) => {
    try {
      await API.post("cart/add/", {
        product_id: productId,
        quantity: 1,
      });
      alert("Added to cart");
    } catch (err) {
      console.error(err);
    }
  };

  // 🔐 AUTH FLOW (FIXED)
  if (!isLoggedIn) {
    return authPage === "login" ? (
      <Login
        onLogin={() => setIsLoggedIn(true)}
        onSwitchToRegister={() => setAuthPage("register")}
      />
    ) : (
      <Register
        onSwitchToLogin={() => setAuthPage("login")}
      />
    );
  }

  return (
    <>
      {/* 🔝 Navbar */}
      <div className="navbar">
        <div>🛒 MyStore</div>

        <div>
          <button onClick={() => setPage("products")}>Products</button>
          <button onClick={() => setPage("cart")}>Cart</button>
          <button
            onClick={() => {
              localStorage.removeItem("token");
              setIsLoggedIn(false);
              setAuthPage("login"); // reset auth page
            }}
          >
            Logout
          </button>
        </div>
      </div>

      <div className="container">
        {/* 🛒 Cart */}
        {page === "cart" && (
          <Cart onCheckout={() => setPage("checkout")} />
        )}

        {/* 📦 Checkout */}
        {page === "checkout" && (
          <Checkout
            onSuccess={(orderId) => {
              setOrderId(orderId);
              setPage("payment");
            }}
          />
        )}

        {/* 💳 Payment */}
        {page === "payment" && (
          <Payment orderId={orderId} />
        )}

        {/* 🛍️ Products */}
        {page === "products" && (
          <>
            <h2>Products</h2>

            <div style={{ display: "flex", flexWrap: "wrap" }}>
              {products.map((product) => (
                <div key={product.id} className="card">
                  <h3>{product.name}</h3>
                  <p>{product.description}</p>
                  <p>₹ {product.price}</p>
                  <p>Stock: {product.inventory_count}</p>

                  <button
                    className="btn btn-primary"
                    onClick={() => addToCart(product.id)}
                  >
                    Add to Cart
                  </button>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </>
  );
}

export default App;