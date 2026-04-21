import { useCallback, useEffect, useMemo, useState } from "react";
import { api, extractError } from "../lib/api";
import type { Product, Reservation } from "../types";

type Filter = "all" | "confirmed" | "cancelled" | "expired";

const filterEndpoints: Record<Filter, string> = {
  all: "/reserve/all",
  confirmed: "/reserve/all_confirmed",
  cancelled: "/reserve/all_cancelled",
  expired: "/reserve/all_expired",
};

const filterLabels: Record<Filter, string> = {
  all: "All",
  confirmed: "Confirmed",
  cancelled: "Cancelled",
  expired: "Expired",
};

function statusLabel(r: Reservation): {
  label: string;
  cls: string;
} {
  if (r.is_confirmed === true)
    return { label: "Confirmed", cls: "bg-emerald-100 text-emerald-700" };
  if (r.is_confirmed === false)
    return { label: "Cancelled", cls: "bg-rose-100 text-rose-700" };
  return { label: "Pending", cls: "bg-amber-100 text-amber-700" };
}

function normalizeList(data: unknown): Reservation[] {
  if (Array.isArray(data)) return data as Reservation[];
  if (data && typeof data === "object") return Object.values(data) as Reservation[];
  return [];
}

export default function Reservations() {
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<Filter>("all");

  const [selectedProductId, setSelectedProductId] = useState<string>("");
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState<string | null>(null);

  const productById = useMemo(() => {
    const m = new Map<number, Product>();
    for (const p of products) m.set(p.id, p);
    return m;
  }, [products]);

  const loadReservations = useCallback(
    async (which: Filter) => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.get(filterEndpoints[which]);
        setReservations(normalizeList(res.data));
      } catch (err) {
        setError(extractError(err, "Failed to load reservations"));
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const loadProducts = useCallback(async () => {
    try {
      const res = await api.get<Product[]>("/products/all");
      setProducts(res.data);
      if (res.data.length > 0 && !selectedProductId) {
        setSelectedProductId(String(res.data[0].id));
      }
    } catch {
      /* ignored — products page shows errors */
    }
  }, [selectedProductId]);

  useEffect(() => {
    loadProducts();
  }, [loadProducts]);

  useEffect(() => {
    loadReservations(filter);
  }, [filter, loadReservations]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedProductId) return;
    setCreating(true);
    setCreateError(null);
    try {
      await api.post("/reserve", {
        product_id: Number(selectedProductId),
      });
      await loadReservations(filter);
      await loadProducts();
    } catch (err) {
      setCreateError(extractError(err, "Failed to create reservation"));
    } finally {
      setCreating(false);
    }
  };

  const handleConfirm = async (id: number) => {
    try {
      await api.patch("/reserve/confirm", null, { params: { reservation_id: id } });
      await loadReservations(filter);
      await loadProducts();
    } catch (err) {
      setError(extractError(err, "Failed to confirm reservation"));
    }
  };

  const handleCancel = async (id: number) => {
    if (!confirm("Cancel this reservation?")) return;
    try {
      await api.delete("/reserve/cancel", { params: { reservation_id: id } });
      await loadReservations(filter);
      await loadProducts();
    } catch (err) {
      setError(extractError(err, "Failed to cancel reservation"));
    }
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Reservations</h1>
        <p className="text-slate-500 mt-1">
          Reserve products and track their status
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="card p-6 sticky top-24">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">
              New reservation
            </h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="label" htmlFor="product">
                  Product
                </label>
                <select
                  id="product"
                  className="input"
                  value={selectedProductId}
                  onChange={(e) => setSelectedProductId(e.target.value)}
                  required
                >
                  <option value="" disabled>
                    Choose a product
                  </option>
                  {products.map((p) => (
                    <option key={p.id} value={p.id} disabled={p.stock <= 0}>
                      {p.name} ({p.stock} in stock)
                    </option>
                  ))}
                </select>
              </div>

              {createError && (
                <div className="rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-sm p-3">
                  {createError}
                </div>
              )}

              <button
                type="submit"
                disabled={creating || !selectedProductId}
                className="btn-primary w-full"
              >
                {creating ? "Reserving..." : "Reserve"}
              </button>
            </form>
          </div>
        </div>

        <div className="lg:col-span-2 space-y-4">
          <div className="flex gap-2 flex-wrap">
            {(Object.keys(filterLabels) as Filter[]).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={
                  filter === f
                    ? "btn-primary"
                    : "btn-secondary"
                }
              >
                {filterLabels[f]}
              </button>
            ))}
          </div>

          {error && (
            <div className="rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-sm p-3">
              {error}
            </div>
          )}

          {loading ? (
            <div className="text-slate-500 text-sm">Loading...</div>
          ) : reservations.length === 0 ? (
            <div className="card p-8 text-center text-slate-500">
              No reservations in this view
            </div>
          ) : (
            <div className="space-y-3">
              {reservations.map((r) => {
                const status = statusLabel(r);
                const product = productById.get(r.product_id);
                return (
                  <div
                    key={r.id}
                    className="card p-5 flex items-center justify-between gap-4 flex-wrap"
                  >
                    <div className="min-w-0">
                      <div className="flex items-center gap-3">
                        <span className="text-sm text-slate-400">
                          Reservation #{r.id}
                        </span>
                        <span className={`badge ${status.cls}`}>
                          {status.label}
                        </span>
                      </div>
                      <div className="font-medium text-slate-900 mt-1">
                        {product ? product.name : `Product #${r.product_id}`}
                      </div>
                      <div className="text-sm text-slate-500">
                        User #{r.user_id}
                      </div>
                    </div>
                    <div className="flex gap-2">
                      {r.is_confirmed === null || r.is_confirmed === undefined ? (
                        <button
                          className="btn-primary"
                          onClick={() => handleConfirm(r.id)}
                        >
                          Confirm
                        </button>
                      ) : null}
                      {r.is_confirmed !== false && (
                        <button
                          className="btn-danger"
                          onClick={() => handleCancel(r.id)}
                        >
                          Cancel
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
