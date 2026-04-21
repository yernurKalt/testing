import { useEffect, useState } from "react";
import { api, extractError } from "../lib/api";
import type { User } from "../types";

export default function Users() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    api
      .get<User[]>("/users/all")
      .then((res) => {
        if (!cancelled) setUsers(res.data);
      })
      .catch((err) => {
        if (!cancelled) setError(extractError(err, "Failed to load users"));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-900">Users</h1>
        <p className="text-slate-500 mt-1">All registered users</p>
      </div>

      {error && (
        <div className="rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-sm p-3 mb-4">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-slate-500 text-sm">Loading...</div>
      ) : users.length === 0 ? (
        <div className="card p-8 text-center text-slate-500">No users yet</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {users.map((u) => (
            <div key={u.id} className="card p-5 flex items-center gap-4">
              <div className="h-12 w-12 rounded-full bg-gradient-to-br from-brand-300 to-brand-500 grid place-items-center text-white font-semibold">
                {u.username.charAt(0).toUpperCase()}
              </div>
              <div className="min-w-0">
                <div className="font-medium text-slate-900 truncate">
                  {u.username}
                </div>
                <div className="text-sm text-slate-500 truncate">{u.email}</div>
                <div className="text-xs text-slate-400 mt-0.5">ID #{u.id}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
