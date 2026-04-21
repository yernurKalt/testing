import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
    isActive
      ? "bg-brand-100 text-brand-700"
      : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
  }`;

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-brand-400 to-brand-600 grid place-items-center text-white font-bold">
                J
              </div>
              <span className="font-semibold text-slate-900">Jobify</span>
            </div>
            <nav className="flex items-center gap-1">
              <NavLink to="/products" className={navLinkClass}>
                Products
              </NavLink>
              <NavLink to="/reservations" className={navLinkClass}>
                Reservations
              </NavLink>
              <NavLink to="/users" className={navLinkClass}>
                Users
              </NavLink>
            </nav>
          </div>
          <div className="flex items-center gap-3">
            {user && (
              <div className="text-right hidden sm:block">
                <div className="text-sm font-medium text-slate-900">
                  {user.username}
                </div>
                <div className="text-xs text-slate-500">{user.email}</div>
              </div>
            )}
            <button onClick={handleLogout} className="btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </header>
      <main className="flex-1">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
