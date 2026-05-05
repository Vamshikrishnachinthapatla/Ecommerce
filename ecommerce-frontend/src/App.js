import React, { useEffect, useState } from "react";
import API from "./api";
import Login from "./pages/Login";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import Payment from "./pages/Payment";
import "./App.css";

function App() {
  const [products, setProducts] = useState([]);
  const [page, setPage] = useState("products");
  const [orderId, setOrderId] = useState(null);
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

  if (!isLoggedIn) {
    return <Login onLogin={() => setIsLoggedIn(true)} />;
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
            }}
          >
            Logout
          </button>
        </div>
      </div>

      <div className="container">
        {/* Pages */}
        {page === "cart" && (
          <Cart onCheckout={() => setPage("checkout")} />
        )}

        {page === "checkout" && (
          <Checkout
            onSuccess={(orderId) => {
              setOrderId(orderId);
              setPage("payment");
            }}
          />
        )}

        {page === "payment" && (
          <Payment orderId={orderId} />
        )}

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