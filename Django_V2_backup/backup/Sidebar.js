import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
    FiLayout, 
    FiArchive, 
    FiClipboard, 
    FiUser, 
    FiDollarSign,
    FiSettings,
    FiMenu,
    FiPlusCircle,
    FiShoppingCart,
    FiList,
    FiFileText
} from 'react-icons/fi';
import './Sidebar.css';

const SidebarLink = ({ href, icon: Icon, label, isCollapsed }) => {
    const isActive = window.location.pathname === href;

    return (
        <Link to={href}>
            <div className={`sidebar-link ${isCollapsed ? 'collapsed' : ''} ${isActive ? 'active' : ''}`}>
                <Icon className="sidebar-icon" />
                {!isCollapsed && <span className="sidebar-label">{label}</span>}
            </div>
        </Link>
    );
};

const Sidebar = () => {
    const [isCollapsed, setIsCollapsed] = useState(false);

    const toggleSidebar = () => {
        setIsCollapsed(!isCollapsed);
    };

    return (
        <div className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
            {/* Top Logo Section */}
            <div className="sidebar-header">
                <img 
                    src="/logo.png" 
                    alt="logo" 
                    className="sidebar-logo"
                />
                {!isCollapsed && <h1 className="sidebar-title">INVENTORY</h1>}
                <button className="collapse-button" onClick={toggleSidebar}>
                    <FiMenu />
                </button>
            </div>

            {/* Navigation Links */}
            <div className="sidebar-links">
                <SidebarLink 
                    href="/dashboard" 
                    icon={FiLayout} 
                    label="Dashboard" 
                    isCollapsed={isCollapsed} 
                />
                <SidebarLink 
                    href="/products" 
                    icon={FiArchive} 
                    label="Products" 
                    isCollapsed={isCollapsed} 
                />
                <SidebarLink 
                    href="/add" 
                    icon={FiPlusCircle} 
                    label="Add Product" 
                    isCollapsed={isCollapsed} 
                />
                <SidebarLink 
                    href="/add-purchase" 
                    icon={FiShoppingCart} 
                    label="Add Purchase" 
                    isCollapsed={isCollapsed} 
                />
                <SidebarLink 
                    href="/purchase-history" 
                    icon={FiList} 
                    label="Purchase History" 
                    isCollapsed={isCollapsed} 
                />
                <SidebarLink 
                    href="/users" 
                    icon={FiUser} 
                    label="Users" 
                    isCollapsed={isCollapsed} 
                />
                <SidebarLink 
                    href="/settings" 
                    icon={FiSettings} 
                    label="Settings" 
                    isCollapsed={isCollapsed} 
                />
                <SidebarLink 
                    href="/expenses" 
                    icon={FiDollarSign} 
                    label="Expenses" 
                    isCollapsed={isCollapsed} 
                />
                <SidebarLink 
                    href="/reports" 
                    icon={FiFileText} 
                    label="Reports" 
                    isCollapsed={isCollapsed} 
                />
            </div>

            {/* Footer */}
            {!isCollapsed && (
                <div className="sidebar-footer">
                    <p>&copy; 2024 Inventory</p>
                </div>
            )}
        </div>
    );
};

export default Sidebar;
