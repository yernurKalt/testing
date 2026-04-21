import { useEffect, useState } from "react";
import { api, extractError } from "../lib/api";
import type { Product } from "../types";

interface FormState {
  name: string;
  stock: string;
}

const emptyForm: FormState = { name: "", stock: "0" };

export default function Products() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [form, setForm] = useState<FormState>(emptyForm);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  const loadProducts = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get<Product[]>("/products/all");
      setProducts(res.data);
    } catch (err) {
      setError(extractError(err, "Failed to load products"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const resetForm = () => {
    setForm(emptyForm);
    setEditingId(null);
    setFormError(null);
  };

  const startEdit = (p: Product) => {
    setEditingId(p.id);
    setForm({ name: p.name, stock: String(p.stock) });
    setFormError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setSubmitting(true);
    try {
      const stockNum = Number(form.stock);
      if (Number.isNaN(stockNum) || stockNum < 0) {
        throw new Error("Stock must be a non-negative number");
      }
      if (editingId !== null) {
        await api.patch(`/products/${editingId}`, {
          name: form.name,
          stock: stockNum,
        });
      } else {
        await api.post("/products/", {
          name: form.name,
          initialStock: stockNum,
        });
      }
      resetForm();
      await loadProducts();
    } catch (err) {
      setFormError(extractError(err, "Failed to save product"));
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this product?")) return;
    try {
      await api.delete(`/products/${id}`);
      await loadProducts();
    } catch (err) {
      setError(extractError(err, "Failed to delete product"));
    }
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Products</h1>
        <p className="text-slate-500 mt-1">
          Create, update, and delete your inventory
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="card p-6 sticky top-24">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">
              {editingId !== null ? "Edit product" : "New product"}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="label" htmlFor="name">
                  Name
                </label>
                <input
                  id="name"
                  className="input"
                  value={form.name}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, name: e.target.value }))
                  }
                  required
                />
              </div>
              <div>
                <label className="label" htmlFor="stock">
                  {editingId !== null ? "Stock" : "Initial stock"}
                </label>
                <input
                  id="stock"
                  type="number"
                  min={0}
                  className="input"
                  value={form.stock}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, stock: e.target.value }))
                  }
                  required
                />
              </div>

              {formError && (
                <div className="rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-sm p-3">
                  {formError}
                </div>
              )}

              <div className="flex gap-2">
                <button
                  type="submit"
                  disabled={submitting}
                  className="btn-primary flex-1"
                >
                  {submitting
                    ? "Saving..."
                    : editingId !== null
                    ? "Save changes"
                    : "Create product"}
                </button>
                {editingId !== null && (
                  <button
                    type="button"
                    onClick={resetForm}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                )}
              </div>
            </form>
          </div>
        </div>

        <div className="lg:col-span-2">
          {error && (
            <div className="rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-sm p-3 mb-4">
              {error}
            </div>
          )}
          {loading ? (
            <div className="text-slate-500 text-sm">Loading...</div>
          ) : products.length === 0 ? (
            <div className="card p-8 text-center text-slate-500">
              No products yet. Create one on the left.
            </div>
          ) : (
            <div className="card overflow-hidden">
              <table className="w-full">
                <thead className="bg-slate-50 text-xs uppercase tracking-wider text-slate-500">
                  <tr>
                    <th className="text-left px-5 py-3 font-medium">ID</th>
                    <th className="text-left px-5 py-3 font-medium">Name</th>
                    <th className="text-left px-5 py-3 font-medium">Stock</th>
                    <th className="px-5 py-3"></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {products.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-50">
                      <td className="px-5 py-3 text-sm text-slate-500">
                        #{p.id}
                      </td>
                      <td className="px-5 py-3 text-sm font-medium text-slate-900">
                        {p.name}
                      </td>
                      <td className="px-5 py-3">
                        <span
                          className={`badge ${
                            p.stock > 0
                              ? "bg-emerald-100 text-emerald-700"
                              : "bg-rose-100 text-rose-700"
                          }`}
                        >
                          {p.stock > 0 ? `${p.stock} in stock` : "Out of stock"}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-right">
                        <div className="flex gap-2 justify-end">
                          <button
                            className="btn-ghost"
                            onClick={() => startEdit(p)}
                          >
                            Edit
                          </button>
                          <button
                            className="btn-danger"
                            onClick={() => handleDelete(p.id)}
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
