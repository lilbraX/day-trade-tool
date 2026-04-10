import Link from "next/link";

export function Nav() {
  return (
    <nav className="nav">
      <Link href="/dashboard">Dashboard</Link>
      <Link href="/trades">Trades</Link>
      <Link href="/import">Import</Link>
      <Link href="/settings">Settings</Link>
    </nav>
  );
}
