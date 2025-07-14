// =============== CART LOGIC USING LOCAL STORAGE ===============

function getCart() {
  return JSON.parse(localStorage.getItem('cart')) || [];
}

function saveCart(cart) {
  localStorage.setItem('cart', JSON.stringify(cart));
}

function addToCart(productId) {
  let cart = getCart();
  let found = cart.find(item => item.id === productId);

  if (found) {
    found.qty += 1;
  } else {
    cart.push({ id: productId, qty: 1 });
  }

  saveCart(cart);
  alert("Item added to cart!");
}

function removeFromCart(productId) {
  let cart = getCart();
  cart = cart.filter(item => item.id !== productId);
  saveCart(cart);
  renderCart(); // update UI
}

function renderCart() {
  const cartItemsDiv = document.getElementById('cart-items');
  const totalPriceDiv = document.getElementById('total-price');

  if (!cartItemsDiv || !totalPriceDiv) return;

  const dummyProducts = {
    1: { name: "Face Cream", price: 499 },
    2: { name: "Lip Balm", price: 249 },
    3: { name: "Hair Serum", price: 699 }
    // Add more dummy products if needed
  };

  const cart = getCart();
  cartItemsDiv.innerHTML = "";
  let total = 0;

  if (cart.length === 0) {
    cartItemsDiv.innerHTML = "<p>Your cart is empty.</p>";
    totalPriceDiv.innerHTML = "";
    return;
  }

  cart.forEach(item => {
    const product = dummyProducts[item.id];
    const subtotal = product.price * item.qty;
    total += subtotal;

    const itemDiv = document.createElement('div');
    itemDiv.className = 'cart-item';
    itemDiv.innerHTML = `
      <p><strong>${product.name}</strong> x ${item.qty} = ₹${subtotal}</p>
      <button onclick="removeFromCart(${item.id})" class="btn remove">Remove</button>
    `;
    cartItemsDiv.appendChild(itemDiv);
  });

  totalPriceDiv.innerText = "Total: ₹" + total;
}

// Run on cart page
if (window.location.pathname.includes("cart")) {
  document.addEventListener("DOMContentLoaded", renderCart);
}
