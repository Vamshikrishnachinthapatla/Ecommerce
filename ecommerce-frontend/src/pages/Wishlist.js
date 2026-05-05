import { useEffect, useState } from "react";
import API from "../api";

function Wishlist() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    API.get("wishlist/").then((res) => setItems(res.data));
  }, []);

  return (
    <div>
      <h2>Wishlist</h2>

      {items.map((item) => (
        <div key={item.id}>
          <h4>{item.product_name}</h4>
          <p>₹{item.price}</p>
        </div>
      ))}
    </div>
  );
}

export default Wishlist;