import { useEffect, useState } from "react";
import API from "../api";

function Products() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    API.get("products/")
      .then((res) => setProducts(res.data))
      .catch((err) => console.log(err));
  }, []);

  const addToCart = async (id) => {
    await API.post("cart/add/", {
      product_id: id,
      quantity: 1,
    });
    alert("Added to cart");
  };

  const toggleWishlist = async (id) => {
    await API.post("wishlist/toggle/", {
      product_id: id,
    });
    alert("Wishlist updated");
  };

  return (
    <div>
      <h2>Products</h2>

      {products.map((p) => (
        <div key={p.id}>
          <h3>{p.name}</h3>
          <p>₹{p.price}</p>

          <button onClick={() => addToCart(p.id)}>Add to Cart</button>
          <button onClick={() => toggleWishlist(p.id)}>❤️ Wishlist</button>
        </div>
      ))}
    </div>
  );
}

export default Products;